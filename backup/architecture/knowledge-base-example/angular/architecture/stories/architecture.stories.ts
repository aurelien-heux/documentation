/**
 * Storybook stories (CSF 3, @storybook/angular) for @aitoolbox/architecture.
 * Each story is one component state from design-system/archimate/components.md.
 * Theme: the toolbar toggle adds `dark` to <html> (see .storybook/preview.ts); styles/tokens-bridge.css + archimate.css are loaded there.
 */
import type { Meta, StoryObj } from '@storybook/angular';
import { moduleMetadata } from '@storybook/angular';
import {
  AtbAsdSectionComponent, AtbCheckRowComponent, AtbDecisionChipComponent, AtbReadinessChipComponent,
  AxChangeComponent, AxFigureComponent, AxRelationshipComponent, AxTileComponent, AxTrackComponent, AX_TYPES, AxType,
} from '../src/public-api';

const PLATEAUS = [{ tag: 'baseline', title: 'Baseline', short: 'B' }, { tag: 'transition-1', title: 'Transition 1', short: 'T1' }, { tag: 'target', title: 'Target', short: 'T' }];
const imports = [AxFigureComponent, AxTileComponent, AxChangeComponent, AxTrackComponent, AxRelationshipComponent, AtbReadinessChipComponent, AtbDecisionChipComponent, AtbCheckRowComponent, AtbAsdSectionComponent];

const meta: Meta = { title: 'Architecture', decorators: [moduleMetadata({ imports })], parameters: { layout: 'padded' } };
export default meta;

export const Figure: StoryObj<AxFigureComponent> = {
  name: 'Figure · sizes and states',
  render: () => ({
    template: `
      <div style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end">
        <atb-ax-figure type="application-component" name="environments Module" size="s" />
        <atb-ax-figure type="business-object" name="Reservation" size="m" />
        <atb-ax-figure type="business-process" name="Request Deployment" size="l" />
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:20px;margin-top:24px">
        <atb-ax-figure type="artifact" name="Environment descriptor" />
        <atb-ax-figure type="application-interface" name="Deployment API" [clickable]="true" />
        <atb-ax-figure type="data-object" name="Deployment record" [selected]="true" />
        <atb-ax-figure type="application-component" name="Booking sheet" [retired]="true" change="retired" />
        <atb-ax-figure type="technology-service" name="CTX-INT Git connector" change="new" />
      </div>`,
  }),
};

export const FigureEveryType: StoryObj = {
  name: 'Figure · every type',
  render: () => ({
    props: { types: Object.keys(AX_TYPES) as AxType[], names: AX_TYPES },
    template: `<div style="display:flex;flex-wrap:wrap;gap:16px">
      @for (t of types; track t) { <atb-ax-figure [type]="t" [name]="names[t].name" size="s" /> }
    </div>`,
  }),
};

export const Tile: StoryObj = {
  name: 'Type tile',
  render: () => ({
    props: { types: ['capability', 'business-actor', 'application-component', 'node', 'equipment', 'goal', 'work-package', 'location'] },
    template: `<div style="display:grid;gap:12px">
      @for (t of types; track t) { <div style="display:flex;align-items:center;gap:10px"><atb-ax-tile [type]="t" /><atb-ax-tile [type]="t" [large]="true" /><span>{{ t }}</span></div> }
      <div style="display:flex;align-items:center;gap:10px"><atb-ax-tile /><atb-ax-tile neutralGlyph="document" /><span>neutral: DD file · ADR</span></div>
    </div>`,
  }),
};

export const Change: StoryObj = {
  name: 'Change chip',
  render: () => ({ template: `<div style="display:flex;gap:12px;flex-wrap:wrap"><atb-ax-change change="new" /><atb-ax-change change="changed" /><atb-ax-change change="retired" /><atb-ax-change change="unchanged" /></div>` }),
};

export const Track: StoryObj = {
  name: 'Plateau track',
  render: () => ({
    props: { plateaus: PLATEAUS },
    template: `<div style="display:grid;gap:12px;justify-items:start">
      <atb-ax-track [plateaus]="plateaus" [member]="['baseline']" />
      <atb-ax-track [plateaus]="plateaus" [member]="['transition-1','target']" />
      <atb-ax-track [plateaus]="plateaus" [member]="['baseline','transition-1','target']" />
    </div>`,
  }),
};

export const Relationship: StoryObj = {
  name: 'Relationship line',
  render: () => ({
    props: { types: ['composition', 'aggregation', 'assignment', 'realization', 'serving', 'access', 'influence', 'triggering', 'flow', 'specialization', 'association'] },
    template: `<div style="display:grid;gap:10px">@for (t of types; track t) { <atb-ax-relationship [type]="t" /> }<atb-ax-relationship type="realization" [highlight]="true" /></div>`,
  }),
};

export const Readiness: StoryObj = {
  name: 'Readiness chip',
  render: () => ({ template: `<div style="display:flex;gap:12px;flex-wrap:wrap"><atb-readiness-chip readiness="ready" /><atb-readiness-chip readiness="attention" /><atb-readiness-chip readiness="blocked" /></div>` }),
};

export const Decision: StoryObj = {
  name: 'Reviewer decision',
  render: () => ({
    props: { ds: ['approved', 'approved-with-conditions', 'changes-requested', 'rejected', 'pending', 'not-required'] },
    template: `<div style="display:flex;gap:12px;flex-wrap:wrap">@for (d of ds; track d) { <atb-decision-chip [decision]="d" /> }</div>`,
  }),
};

export const CheckRows: StoryObj = {
  name: 'Check row',
  render: () => ({
    props: {
      checks: [
        { id: 'T4', group: 'Traceability', title: 'Every requirement is realized by at least one ABB', severity: 'error', status: 'pass', items: [] },
        { id: 'T6', group: 'Traceability', title: 'Every new or changed application SBB has a detailed design', severity: 'warning', status: 'warn', items: [{ id: 'sbb.environments.jenkins-descriptor-job', title: 'Jenkins descriptor job', message: 'no detailed design yet' }] },
        { id: 'O2', group: 'Ownership & contracts', title: 'Interfaces and events reference a contract file that exists', severity: 'error', status: 'fail', items: [{ id: 'sbb.environments.reservation-api', title: 'Reservation API', message: "contract 'contracts/reservations.openapi.yaml' not found" }] },
      ],
    },
    template: `<div style="max-width:720px">@for (c of checks; track c.id) { <atb-check-row [check]="c" /> }</div>`,
  }),
};

export const AsdSection: StoryObj = {
  name: 'ASD section header',
  render: () => ({
    template: `<div style="display:grid;gap:24px;max-width:720px">
      <atb-asd-section [index]="4" title="Baseline" source="model" sectionId="asd-4"><p>Baseline landscape view.</p></atb-asd-section>
      <atb-asd-section [index]="2" title="Business need" source="written" sectionId="asd-2"><p>Median lead time 26 h.</p></atb-asd-section>
      <atb-asd-section [index]="11" title="Security" source="thin" sectionId="asd-11"><p>Token scope…</p></atb-asd-section>
      <atb-asd-section [index]="12" title="Risks" source="missing" sectionId="asd-12"></atb-asd-section>
    </div>`,
  }),
};
