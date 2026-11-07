#!/bin/zsh
# Storyboard template: copy next to your output folder, edit the steps, run with
#   zsh storyboard.zsh /path/to/out
set -e
# phone instead: REC_W=402 REC_H=874 REC_SCALE=2 (tap dot, no caption pill)
REC_DIR=$1 REC_SESSION=rec source ~/.claude/skills/record-it/scripts/lib.zsh

start "http://localhost:8000/admin.html?lang=en"

# clean start: log out any session left over from an earlier run, then assert it
agent-browser eval "document.querySelector('#btn-logout')?.offsetParent && document.querySelector('#btn-logout').click()" >/dev/null
go "http://localhost:8000/admin.html?lang=en"
[[ $(agent-browser eval "!!document.querySelector('#l-login')?.offsetParent") == true ]] || { echo "not logged out" >&2; exit 1; }

caption "Barbara, Coordinator"; shot 2.5                 # who we are, before anything moves
typeslow "#l-login" barbara
typeslow "#l-pass" barbara; shot 0.4
click "#login-form button"; until_js "!!document.querySelector('#btn-logout')?.offsetParent"
caption ""; shot 2.5                                     # hold the key state long enough to read
echo "count: $(agent-browser eval "document.querySelector('#list-count').innerText")"   # log facts, check them later

mark pick                                                # cue point for the edit, lands in markers.json
click "#admin-list [data-pick]@1"; ab wait 400; shot 2.2
scrollto ".share-card" 40; shot 1.5                      # eased scroll, window or inner scroll container
# choose "#orgpick" "wandsbek"; shot 2.5                 # a <select>, e.g. for an account with a picker

click "#btn-logout"; until_js "!!document.querySelector('#l-login')?.offsetParent"; shot 2
render demo.mp4
