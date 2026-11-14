      <div class="row" style="gap: 8px; padding: 6px 8px 6px 12px; border: 1px dashed #79757F; border-radius: 12px; align-self: flex-start">
        <span style="font-size: 12px; font-weight: 600; color: #48454E" class="ui">Prototype · view as</span>
        <sc-for list="{{roleChips}}" as="r" hint-placeholder-count="3"><button type="button" class="chip" style="height: 28px; font-size: 12px; {{r.style}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button></sc-for>
      </div>