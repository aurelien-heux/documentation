import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButton, MatIconButton } from '@angular/material/button';
import { MatButtonToggle, MatButtonToggleGroup } from '@angular/material/button-toggle';
import { MatCard, MatCardContent, MatCardHeader, MatCardTitle } from '@angular/material/card';
import { MatCheckbox } from '@angular/material/checkbox';
import { MatChipListbox, MatChipOption, MatChipRemove, MatChipRow, MatChipGrid, MatChipInput } from '@angular/material/chips';
import { MatFormField, MatHint, MatLabel } from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { MatInput } from '@angular/material/input';
import { MatRadioButton, MatRadioGroup } from '@angular/material/radio';
import { MatOption, MatSelect } from '@angular/material/select';
import { MatSlideToggle } from '@angular/material/slide-toggle';
import { MatTab, MatTabGroup } from '@angular/material/tabs';
import { MatTooltip } from '@angular/material/tooltip';
import {
  AitAi, AitAiChip, AitBanner, AitBrandLoader, AitConfirm, AitConstructorProgress, AitDanger, AitDisabledReason, AitEmptyState,
  AitGuideLine, AitLogLevel, AitLogo, AitChatbotMark, AitPenOrbit, AitRun, AitRunText, AitSnackBar, AitState, AitStateMark,
  AitStatusChip, AitTonal, AitWorkingDots,
} from '@aitoolbox/ui';

@Component({
  selector: 'app-components',
  imports: [
    FormsModule, MatButton, MatIconButton, MatIcon, MatButtonToggleGroup, MatButtonToggle, MatCard, MatCardHeader, MatCardTitle, MatCardContent,
    MatCheckbox, MatChipListbox, MatChipOption, MatChipRow, MatChipGrid, MatChipInput, MatChipRemove, MatFormField, MatLabel, MatHint,
    MatInput, MatRadioGroup, MatRadioButton, MatSelect, MatOption, MatSlideToggle, MatTabGroup, MatTab, MatTooltip,
    AitAi, AitAiChip, AitBanner, AitBrandLoader, AitConstructorProgress, AitDanger, AitDisabledReason, AitEmptyState, AitGuideLine, AitLogLevel,
    AitLogo, AitChatbotMark, AitPenOrbit, AitRun, AitRunText, AitStateMark, AitStatusChip, AitTonal, AitWorkingDots,
  ],
  templateUrl: './components.page.html',
  styleUrl: './components.page.scss',
})
export class ComponentsPage {
  protected readonly snack = inject(AitSnackBar);
  private readonly confirm = inject(AitConfirm);
  protected readonly states: AitState[] = ['success', 'info', 'warning', 'error'];
  protected readonly progress = signal(35);
  protected readonly view = signal('week');
  protected readonly tags = signal(['env:staging', 'app:billing-api']);

  protected openConfirm(destructive: boolean): void {
    this.confirm
      .open(
        destructive
          ? { title: 'Delete workspace billing-sandbox?', message: 'Its 3 environments are released. Runs and logs are kept for 30 days.', confirmLabel: 'Delete', destructive: true }
          : { title: 'Request the implement Run?', message: 'Workflow jira-feature v2 runs on WI-318, pinned to the approved design.', confirmLabel: 'Request Run' },
      )
      .subscribe((ok) => ok && this.snack.open(destructive ? 'Workspace deleted' : 'Run requested', { state: 'success', action: 'Undo' }));
  }

  protected removeTag(t: string): void {
    this.tags.update((all) => all.filter((x) => x !== t));
  }
}
