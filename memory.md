## Memory

- `frontend/silent-night/src/views/HomeView.vue`: added responsive background images using public assets:
  - Widescreen/default: `/Silent-Night-landscape.png`
  - Mobile/portrait: `/Silent-Night-Portrait.png`

- `frontend/silent-night/src/assets/main.css`: global custom font (`a Theme for murder`) registered via `@font-face` and applied to Quasar heading classes (`text-h1`..`text-h6`).
- `frontend/silent-night/src/assets/main.css`: added `Raven Scream` font and set it as the global `body` font.
- `frontend/silent-night/src/assets/main.css`: increased Quasar `QInput` and `QBtn` font size to `1.2rem` (via `.q-field__native/.q-field__input` and `.q-btn`).
- `frontend/silent-night/src/pages/Game.vue`: gameplay layout is now two-column with `RoleCard` on the left and the players list scroll area on the right.
- `frontend/silent-night/src/util/roles.js`: central lookup for role title/description/image, used by `RoleCard.vue`.
- **Player identity / auth**: the backend no longer shares player ids; players are identified by `username` in the frontend (`players` store selectors use username). Only `currentUser.id` is kept and used for auth when making requests; non-current player ids are stripped if encountered.

