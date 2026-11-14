import { Component, computed, inject, signal } from '@angular/core';
import { MatButton } from '@angular/material/button';
import { MatChipListbox, MatChipOption } from '@angular/material/chips';
import { MatIcon } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import {
  AitConfirm, AitEmptyState, AitRun, AitRunText, AitDanger, AitSnackBar, AitStateMark, AitWorkingDots,
} from '@aitoolbox/ui';

type Status = 'running' | 'awaiting_review' | 'queued' | 'succeeded' | 'failed' | 'cancelled';
interface Run { id: string; wf: string; wi: string; title: string; app: string; status: Status; current: string; note: string; started: string; }

const LABEL: Record<Status, string> = {
  running: 'Running', awaiting_review: 'Awaiting review', queued: 'Queued', succeeded: 'Succeeded', failed: 'Failed', cancelled: 'Cancelled',
};

@Component({
  selector: 'app-runs',
  imports: [MatTableModule, MatButton, MatIcon, MatChipListbox, MatChipOption, AitRun, AitRunText, AitDanger, AitStateMark, AitWorkingDots, AitEmptyState],
  template: `
    <main class="ait-page">
      <div class="head">
        <div>
          <div class="ait-label-medium ait-muted">Workflows ui-design · jira-feature</div>
          <h1 class="ait-headline-large title">Runs</h1>
          <p class="ait-muted intro">UI changes start with a design Run and a review Checkpoint; the approved design then feeds jira-feature.</p>
        </div>
        <button mat-flat-button aitRun (click)="snack.open('Run requested', { state: 'success', action: 'View' })">
          <mat-icon svgIcon="ait:play" />Request Run
        </button>
      </div>

      <mat-chip-listbox aria-label="Filter by status" class="filters" (change)="filter.set($event.value ?? 'all')">
        <mat-chip-option value="all" [selected]="filter() === 'all'">All</mat-chip-option>
        @for (s of statuses; track s) {
          <mat-chip-option [value]="s" [selected]="filter() === s">{{ label[s] }}</mat-chip-option>
        }
      </mat-chip-listbox>

      <div class="ait-table">
        @if (rows().length) {
          <table mat-table [dataSource]="rows()">
            <ng-container matColumnDef="run">
              <th mat-header-cell *matHeaderCellDef>Run</th>
              <td mat-cell *matCellDef="let r"><div class="ait-data">{{ r.id }}</div><div class="ait-body-small ait-muted">{{ r.wf }}</div></td>
            </ng-container>
            <ng-container matColumnDef="item">
              <th mat-header-cell *matHeaderCellDef>Work item</th>
              <td mat-cell *matCellDef="let r"><div class="ait-title-small">{{ r.wi }}</div><div class="ait-body-small ait-muted">{{ r.title }} · <span class="ait-data">{{ r.app }}</span></div></td>
            </ng-container>
            <ng-container matColumnDef="status">
              <th mat-header-cell *matHeaderCellDef>Status</th>
              <td mat-cell *matCellDef="let r">
                <span class="status ait-label-medium">
                  @switch (r.status) {
                    @case ('running') { <ait-working-dots class="slot" label="" aria-hidden="true" /> }
                    @case ('awaiting_review') { <ait-state-mark state="warning" variant="tile" /> }
                    @case ('succeeded') { <ait-state-mark state="success" variant="tile" /> }
                    @case ('failed') { <ait-state-mark state="error" variant="tile" /> }
                    @default { <span class="dot" aria-hidden="true"></span> }
                  }
                  {{ statusLabel(r) }}
                </span>
              </td>
            </ng-container>
            <ng-container matColumnDef="current">
              <th mat-header-cell *matHeaderCellDef class="ait-col-p2">Current Step</th>
              <td mat-cell *matCellDef="let r" class="ait-col-p2"><div class="ait-title-small">{{ r.current }}</div><div class="ait-body-small ait-muted">{{ r.note }}</div></td>
            </ng-container>
            <ng-container matColumnDef="started">
              <th mat-header-cell *matHeaderCellDef class="ait-col-p3">Started</th>
              <td mat-cell *matCellDef="let r" class="ait-col-p3 ait-data">{{ r.started }}</td>
            </ng-container>
            <ng-container matColumnDef="actions">
              <th mat-header-cell *matHeaderCellDef class="end">Actions</th>
              <td mat-cell *matCellDef="let r" class="end">
                @if (r.status === 'failed' || r.status === 'cancelled') {
                  <button mat-button aitRunText><mat-icon svgIcon="ait:play" />Re-run</button>
                }
                <button mat-button>{{ r.status === 'awaiting_review' ? 'Review' : 'View' }}</button>
                @if (r.status === 'running' || r.status === 'queued' || r.status === 'awaiting_review') {
                  <button mat-button aitDanger (click)="cancel(r)">Cancel</button>
                }
              </td>
            </ng-container>
            <tr mat-header-row *matHeaderRowDef="columns"></tr>
            <tr mat-row *matRowDef="let r; columns: columns"></tr>
          </table>
        } @else {
          <ait-empty-state state="info" title="No Runs with this status" cause="Runs of the last 7 days appear here. Change the filter or request a Run.">
            <button mat-button (click)="filter.set('all')">Show all Runs</button>
          </ait-empty-state>
        }
      </div>
    </main>
  `,
  styles: `
    .head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 16px; }
    .title { margin: 4px 0 0; }
    .intro { margin: 4px 0 0; max-width: 720px; }
    .filters { display: block; margin: 24px 0 16px; }
    .status { display: inline-flex; align-items: center; gap: 8px; }
    .slot { width: 20px; justify-content: center; }
    .dot { width: 8px; height: 8px; border-radius: 9999px; border: 2px solid var(--md-sys-color-outline); box-sizing: border-box; margin: 0 6px; }
    td { padding-block: 8px; }
    .ait-data, .status { white-space: nowrap; }
    .end { text-align: right; white-space: nowrap; }
  `,
})
export class RunsPage {
  protected readonly snack = inject(AitSnackBar);
  private readonly confirm = inject(AitConfirm);
  protected readonly label = LABEL;
  protected readonly statuses = Object.keys(LABEL) as Status[];
  protected readonly columns = ['run', 'item', 'status', 'current', 'started', 'actions'];
  protected readonly filter = signal<Status | 'all'>('all');
  private readonly runs: Run[] = [
    { id: 'run-0149', wf: 'ui-design', wi: 'WI-331', title: 'Manage SEPA mandates', app: 'customer-portal', status: 'awaiting_review', current: 'Design review · revision 2', note: '2 of 3 decisions made', started: '11:15' },
    { id: 'run-0148', wf: 'ui-design', wi: 'WI-329', title: 'Dunning letter preview', app: 'billing-portal', status: 'running', current: 'Screenshots', note: '12 of 18 variant × state', started: '11:09' },
    { id: 'run-0147', wf: 'jira-feature', wi: 'WI-318', title: 'Add SEPA mandate export', app: 'billing-api', status: 'running', current: 'Frontend coder · Backend reviewer', note: 'From approved design rev 2', started: '10:02' },
    { id: 'run-0145', wf: 'jira-feature', wi: 'WI-311', title: 'Bump PDF library', app: 'document-service', status: 'queued', current: '—', note: 'Position 1 in queue', started: '—' },
    { id: 'run-0143', wf: 'jira-feature', wi: 'WI-301', title: 'Retry on ledger sync job', app: 'ledger-sync', status: 'succeeded', current: '—', note: 'PR #482 opened', started: '08:55' },
    { id: 'run-0141', wf: 'jira-feature', wi: 'WI-298', title: 'Migrate settings form', app: 'customer-portal', status: 'failed', current: 'Frontend coder', note: 'Tests failed (3)', started: '08:12' },
    { id: 'run-0140', wf: 'jira-feature', wi: 'WI-296', title: 'Remove deprecated export flag', app: 'document-service', status: 'cancelled', current: 'Coders (both lanes)', note: 'by a.heux · wrong Brief', started: '07:58' },
  ];
  protected readonly rows = computed(() => (this.filter() === 'all' ? this.runs : this.runs.filter((r) => r.status === this.filter())));

  protected statusLabel(r: Run): string {
    return LABEL[r.status];
  }

  protected cancel(r: Run): void {
    this.confirm
      .open({ title: `Cancel ${r.id}?`, message: 'Both lanes stop at their next action and the Run ends as Cancelled. Logs and done Steps are kept.', confirmLabel: 'Cancel Run', dismissLabel: 'Keep running', destructive: true })
      .subscribe((ok) => ok && this.snack.open(`${r.id} cancelled`, { state: 'success' }));
  }
}
