import 'zone.js';
import { Component } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import {
  AtbAsdSectionComponent, AtbCheckRowComponent, AtbDecisionChipComponent, AtbReadinessChipComponent,
  AxChangeComponent, AxFigureComponent, AxRelationshipComponent, AxTileComponent, AxTrackComponent, AX_TYPES, AxType,
} from '../src/public-api';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [AxFigureComponent, AxTileComponent, AxChangeComponent, AxTrackComponent, AxRelationshipComponent, AtbReadinessChipComponent, AtbDecisionChipComponent, AtbCheckRowComponent, AtbAsdSectionComponent],
  template: `
  <main style="padding:24px;display:grid;gap:28px;font-family:var(--md-sys-typescale-plain-family);color:var(--md-sys-color-on-surface)">
    <h2 style="margin:0;font:700 18px/24px var(--md-sys-typescale-brand-family)">Figure · sizes and states</h2>
    <div style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end">
      <atb-ax-figure type="application-component" name="environments Module" size="s" />
      <atb-ax-figure type="business-object" name="Reservation" size="m" />
      <atb-ax-figure type="business-process" name="Request Deployment" size="l" />
      <atb-ax-figure type="artifact" name="Environment descriptor" />
      <atb-ax-figure type="application-interface" name="Deployment API" [clickable]="true" />
      <atb-ax-figure type="data-object" name="Deployment record" [selected]="true" />
      <atb-ax-figure type="application-component" name="Booking sheet" [retired]="true" change="retired" />
      <atb-ax-figure type="technology-service" name="CTX-INT Git connector" change="new" />
      <atb-ax-figure type="contract" name="Service level" size="s" /><atb-ax-figure type="deliverable" name="Release notes" size="s" />
      <atb-ax-figure type="product" name="Environments" size="s" /><atb-ax-figure type="goal" name="Self-service" size="s" /><atb-ax-figure type="value" name="Lead time" size="s" />
    </div>
    <h2 style="margin:0;font:700 18px/24px var(--md-sys-typescale-brand-family)">Tiles, change, track, relationships</h2>
    <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:center">
      @for (t of tiles; track t) { <atb-ax-tile [type]="t" /><atb-ax-tile [type]="t" [large]="true" /> }
      <atb-ax-tile /><atb-ax-tile neutralGlyph="document" />
      <atb-ax-change change="new" /><atb-ax-change change="changed" /><atb-ax-change change="retired" /><atb-ax-change change="unchanged" />
      <atb-ax-track [plateaus]="plateaus" [member]="['transition-1','target']" />
    </div>
    <div style="display:grid;gap:8px">@for (r of rels; track r) { <atb-ax-relationship [type]="r" /> }<atb-ax-relationship type="realization" [highlight]="true" /></div>
    <h2 style="margin:0;font:700 18px/24px var(--md-sys-typescale-brand-family)">Review</h2>
    <div style="display:flex;flex-wrap:wrap;gap:12px"><atb-readiness-chip readiness="ready" /><atb-readiness-chip readiness="attention" /><atb-readiness-chip readiness="blocked" />
      @for (d of ds; track d) { <atb-decision-chip [decision]="d" /> }</div>
    <div style="max-width:720px">@for (c of checks; track c.id) { <atb-check-row [check]="c" /> }</div>
    <div style="display:grid;gap:20px;max-width:720px">
      <atb-asd-section [index]="4" title="Baseline" source="model" sectionId="asd-4"><p style="margin:0">Baseline landscape view.</p></atb-asd-section>
      <atb-asd-section [index]="11" title="Security" source="thin" sectionId="asd-11"><p style="margin:0">Token scope…</p></atb-asd-section>
      <atb-asd-section [index]="12" title="Risks" source="missing" sectionId="asd-12"></atb-asd-section>
    </div>
  </main>`,
})
class App {
  tiles: AxType[] = ['capability', 'business-actor', 'application-component', 'node', 'equipment', 'goal', 'work-package', 'location'];
  plateaus = [{ tag: 'baseline', title: 'Baseline', short: 'B' }, { tag: 'transition-1', title: 'Transition 1', short: 'T1' }, { tag: 'target', title: 'Target', short: 'T' }];
  rels: any[] = ['composition', 'aggregation', 'assignment', 'realization', 'serving', 'access', 'influence', 'triggering', 'flow', 'specialization', 'association'];
  ds: any[] = ['approved', 'approved-with-conditions', 'changes-requested', 'rejected', 'pending', 'not-required'];
  checks: any[] = [
    { id: 'T4', group: 'Traceability', title: 'Every requirement is realized by at least one ABB', severity: 'error', status: 'pass', items: [] },
    { id: 'T6', group: 'Traceability', title: 'Every new or changed application SBB has a detailed design', severity: 'warning', status: 'warn', items: [{ id: 'sbb.environments.jenkins-descriptor-job', title: 'Jenkins descriptor job', message: 'no detailed design yet' }] },
    { id: 'O2', group: 'Ownership & contracts', title: 'Interfaces and events reference a contract file that exists', severity: 'error', status: 'fail', items: [{ id: 'sbb.environments.reservation-api', title: 'Reservation API', message: "contract not found" }] },
  ];
  n = Object.keys(AX_TYPES).length;
}
bootstrapApplication(App).catch(e => console.error(e));
