import { Component } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import {
  AX_GLYPHS, AX_RELATIONSHIPS, AX_TYPES, AxChangeComponent, AxFigureComponent, AxRelationshipComponent, AxTileComponent, AxTrackComponent,
} from '../../public-api';

describe('notation data', () => {
  it('has every ArchiMate type with a known glyph and layer', () => {
    const types = Object.keys(AX_TYPES);
    expect(types.length).toBe(62);
    for (const t of types) {
      const i = AX_TYPES[t as keyof typeof AX_TYPES];
      expect(AX_GLYPHS[i.glyph]).toBeTruthy();
      expect(['strategy', 'business', 'application', 'technology', 'physical', 'motivation', 'implementation', 'other']).toContain(i.layer);
    }
    expect(Object.keys(AX_RELATIONSHIPS).length).toBe(11);
  });
  it('gives passive types their own figure', () => {
    expect(AX_TYPES['business-object'].shape).toBe('object');
    expect(AX_TYPES['contract'].shape).toBe('contract');
    expect(AX_TYPES['artifact'].shape).toBe('artifact');
    expect(AX_TYPES['deliverable'].shape).toBe('wave');
    expect(AX_TYPES['product'].shape).toBe('product');
  });
});

@Component({
  standalone: true,
  imports: [AxFigureComponent],
  template: `<atb-ax-figure [type]="type" [name]="name" [size]="size" [clickable]="clickable" [selected]="selected" [retired]="retired" [change]="change" (activate)="n = n + 1" />`,
})
class FigureHost { type: any = 'business-object'; name = 'Reservation'; size: any = 'm'; clickable = false; selected = false; retired = false; change: any = undefined; n = 0; }

describe('atb-ax-figure', () => {
  let fx: ComponentFixture<FigureHost>;
  beforeEach(async () => { await TestBed.configureTestingModule({ imports: [FigureHost] }).compileComponents(); fx = TestBed.createComponent(FigureHost); fx.detectChanges(); });
  const box = () => fx.nativeElement.querySelector('.ax-box') as HTMLElement;

  it('draws the type: layer class, shape class, glyph, name', () => {
    expect(box().className).toContain('ax-l-business');
    expect(box().className).toContain('ax-shape-object');
    expect(box().querySelector('svg')).toBeTruthy();
    expect(box().textContent).toContain('Reservation');
  });
  it('is an image named "<name>, <type>" when static', () => {
    expect(box().getAttribute('role')).toBe('img');
    expect(box().getAttribute('aria-label')).toBe('Reservation, business object');
  });
  it('becomes a button when clickable and emits activate', () => {
    fx.componentInstance.clickable = true; fx.detectChanges();
    expect(box().tagName).toBe('BUTTON');
    expect(box().getAttribute('aria-label')).toBe('Reservation, business object');
    box().click();
    expect(fx.componentInstance.n).toBe(1);
  });
  it('shows selected with aria-current and the ring class', () => {
    fx.componentInstance.selected = true; fx.detectChanges();
    expect(box().getAttribute('aria-current')).toBe('true');
    expect(box().className).toContain('ax-selected');
  });
  it('says retired in the name and shows the change chip', () => {
    fx.componentInstance.retired = true; fx.componentInstance.change = 'retired'; fx.detectChanges();
    expect(box().getAttribute('aria-label')).toContain('retired');
    const chip = fx.nativeElement.querySelector('.ax-change') as HTMLElement;
    expect(chip.className).toContain('retired');
    expect(chip.textContent).toContain('Retired');
  });
  it('applies the size class', () => { fx.componentInstance.size = 'l'; fx.detectChanges(); expect(box().className).toContain('ax-l'); });
  it('marks the and-junction filled', () => { fx.componentInstance.type = 'and-junction'; fx.detectChanges(); expect(box().className).toContain('ax-and'); });
});

@Component({ standalone: true, imports: [AxTileComponent], template: `<atb-ax-tile [type]="type" [large]="large" /><atb-ax-tile neutralGlyph="document" />` })
class TileHost { type: any = 'application-interface'; large = false; }

describe('atb-ax-tile', () => {
  it('is decorative, carries the layer class and the type name as title', async () => {
    await TestBed.configureTestingModule({ imports: [TileHost] }).compileComponents();
    const fx = TestBed.createComponent(TileHost); fx.detectChanges();
    const tiles = fx.nativeElement.querySelectorAll('atb-ax-tile') as NodeListOf<HTMLElement>;
    expect(tiles[0].getAttribute('aria-hidden')).toBe('true');
    expect(tiles[0].className).toContain('ax-l-application');
    expect(tiles[0].getAttribute('title')).toBe('Application interface');
    expect(tiles[1].className).toContain('ax-neutral');
    expect(tiles[1].getAttribute('title')).toBe('Decision record');
    fx.componentInstance.large = true; fx.detectChanges();
    expect(tiles[0].className).toContain('lg');
  });
});

@Component({ standalone: true, imports: [AxChangeComponent, AxTrackComponent, AxRelationshipComponent],
  template: `<atb-ax-change change="new" /><atb-ax-track [plateaus]="ps" [member]="['baseline','target']" /><atb-ax-relationship type="realization" [highlight]="hi" />` })
class MiscHost { ps = [{ tag: 'baseline', title: 'Baseline', short: 'B' }, { tag: 'transition-1', title: 'Transition 1', short: 'T1' }, { tag: 'target', title: 'Target', short: 'T' }]; hi = false; }

describe('change chip, plateau track, relationship line', () => {
  let fx: ComponentFixture<MiscHost>;
  beforeEach(async () => { await TestBed.configureTestingModule({ imports: [MiscHost] }).compileComponents(); fx = TestBed.createComponent(MiscHost); fx.detectChanges(); });
  it('change chip: class and word', () => {
    const c = fx.debugElement.query(By.directive(AxChangeComponent)).nativeElement as HTMLElement;
    expect(c.className).toContain('ax-change'); expect(c.className).toContain('new'); expect(c.textContent).toContain('New');
  });
  it('track: one cell per plateau, members on, label lists them', () => {
    const t = fx.debugElement.query(By.directive(AxTrackComponent)).nativeElement as HTMLElement;
    const cells = t.querySelectorAll('span');
    expect(cells.length).toBe(3);
    expect(cells[0].className).toContain('on'); expect(cells[1].className).not.toContain('on'); expect(cells[2].className).toContain('on');
    expect(t.getAttribute('aria-label')).toBe('In Baseline, Target');
  });
  it('relationship: dotted realization with a hollow triangle, highlight class', () => {
    const svg = fx.nativeElement.querySelector('svg.ax-rel') as SVGElement;
    expect(svg.getAttribute('aria-label')).toBe('Realization, dotted line');
    expect(svg.querySelector('line')!.getAttribute('stroke-dasharray')).toBe('2 3');
    expect(svg.querySelector('.mk-open')).toBeTruthy();
    fx.componentInstance.hi = true; fx.detectChanges();
    expect(svg.getAttribute('class')).toContain('hi');
  });
});
