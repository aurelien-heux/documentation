import type { Preview } from '@storybook/angular';
import '../src/styles/tokens-bridge.css';   // only here: the app loads css/tokens.css instead
import '../src/styles/archimate.css';

/** Theme toolbar: sets html.light / html.dark like the AIToolbox app. */
const preview: Preview = {
  globalTypes: { theme: { description: 'Theme', toolbar: { icon: 'mirror', items: ['light', 'dark'], dynamicTitle: true } } },
  initialGlobals: { theme: 'light' },
  decorators: [
    (story, ctx) => {
      const h = document.documentElement;
      h.classList.toggle('dark', ctx.globals['theme'] === 'dark');
      h.classList.toggle('light', ctx.globals['theme'] !== 'dark');
      return story();
    },
  ],
  parameters: { a11y: { test: 'error' }, backgrounds: { disable: true } },
};
export default preview;
