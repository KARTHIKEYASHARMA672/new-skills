# record-it helpers. Source from a zsh storyboard script:
#   REC_DIR=/path/to/out REC_SESSION=rec source ~/.claude/skills/record-it/scripts/lib.zsh
# Every frame is a screenshot with a hold time; render() stitches them with ffmpeg.
# Phone: REC_W=402 REC_H=874 REC_SCALE=2 (CSS px + device scale; frames come out 804x1748).

: ${REC_DIR:?set REC_DIR to an output folder outside the repo}
: ${REC_SESSION:=rec}
: ${REC_W:=1920} ${REC_H:=1080} ${REC_SCALE:=1} ${REC_FPS:=30}
(( REC_W < 700 )) && : ${REC_TOUCH:=1} ${REC_CAPTIONS:=0}  # narrow viewport: tap dot, no caption pill
: ${REC_TOUCH:=0} ${REC_CAPTIONS:=1}
export AGENT_BROWSER_SESSION=$REC_SESSION
typeset -g REC_OUT=$REC_DIR REC_LIB=${0:A:h}    # kept: a "VAR=x source" prefix only lasts for the source
typeset -g REC_VW=$REC_W REC_VH=$REC_H REC_VS=$REC_SCALE REC_R=$REC_FPS REC_T=$REC_TOUCH REC_C=$REC_CAPTIONS
F=$REC_OUT/frames; L=$REC_OUT/list.txt
rm -rf $F; mkdir -p $F; : > $L
n=0; nf=0; CX=$((REC_W / 2)); CY=$((REC_H / 2)); CAP=""
typeset -gA MARKS

zmodload zsh/mathfunc                                   # int() and rint() in shot()
ab() { agent-browser "$@" >/dev/null; }                 # quiet; functions, since zsh won't split "$AB"
js() { { cat $REC_LIB/overlay.js; echo "$1"; } | agent-browser eval --stdin; }
q()  { python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))'; }   # JS string literal

# put overlay, cursor and caption back; call after every navigation or reload
sync() { js "__touch($REC_T); __pos($CX,$CY); __cap($(printf '%s' "$CAP" | q))" >/dev/null; }

# one frame held for $1 seconds, rounded to whole video frames so marks match the MP4 exactly
shot() {
  local k=$(( int(rint($1 * REC_R)) )); (( k < 1 )) && k=1
  n=$((n + 1)); nf=$((nf + k))
  local f=$(printf "%s/%04d.png" $F $n); agent-browser screenshot $f >/dev/null
  printf "file '%s'\nduration %.6f\n" $f $(( k * 1.0 / REC_R )) >> $L
}

# record the current video time under a name; render() writes all marks to markers.json
mark() { MARKS[$1]=$(printf "%.3f" $(( nf * 1.0 / REC_R ))); echo "mark $1 ${MARKS[$1]}"; }

caption() { (( REC_C )) || return 0; CAP="$1"; sync; }

# glide the cursor to the center of a selector (+ optional x offset), eased, 6-12 steps
glide() {
  local c=$(js "__ctr('$1')" | tr -d '"')
  [[ $c == missing ]] && { echo "glide: no element for $1" >&2; return 1; }
  local tx=$(( ${c%,*} + ${2:-0} )) ty=${c#*,}
  for p in $(python3 -c "
import math
s=max(6,min(12,int(math.hypot($tx-$CX,$ty-$CY)/70)))
for i in range(1,s+1):
  t=i/s; e=t*t*(3-2*t); print(f'{round($CX+($tx-$CX)*e)},{round($CY+($ty-$CY)*e)}')"); do
    js "__pos(${p%,*},${p#*,})" >/dev/null; shot 0.04
  done
  CX=$tx; CY=$ty; shot 0.25
}

ripple() { for d in 18 34 50; do js "__rip($CX,$CY,$d)" >/dev/null; shot 0.05; done; js "__rip(0,0,0)" >/dev/null; }

# show the cursor clicking, then click via JS (agent-browser clicks can miss under sticky headers)
click() {
  glide "$1" ${2:-0}; ripple
  local sel=$1 idx=0; [[ $sel == *@<-> ]] && { idx=${sel##*@}; sel=${sel%@*}; }
  agent-browser eval "document.querySelectorAll($(printf '%s' "$sel" | q))[$idx].click()" >/dev/null
}

# smooth-scroll until SEL's top sits $2 px below the viewport top (default 120), eased, 12 frames.
# Finds the element's own scroll container, so pages that scroll inside a <main> work too.
scrollto() {
  local r=$(js "__scrollPlan($(printf '%s' "$1" | q), ${2:-120})" | tr -d '"')
  [[ $r == missing ]] && { echo "scrollto: no element for $1" >&2; return 1; }
  for i in {1..12}; do js "__scrollStep($i, 12)" >/dev/null; shot 0.04; done
  shot 0.3
}

# click into a field, then type one character per frame
typeslow() {
  glide "$1" ${3:-40}; ripple; ab focus "$1"; shot 0.3
  for ch in ${(s::)2}; do ab type "$1" "$ch"; shot 0.13; done
}

# pick a <select> value; the native option list never shows in headless screenshots
choose() { glide "$1"; ripple; ab focus "$1"; shot 0.5; ab select "$1" "$2"; ab wait 500; }

# wait for a JS condition, then restore the overlay (use after anything that reloads)
until_js() { ab wait --fn "$1"; ab wait ${2:-500}; sync; }

go() { ab open "$1"; ab wait --load networkidle; ab wait 400; sync; }

start() { ab set viewport $REC_VW $REC_VH $REC_VS; go "$1"; }

# stitch frames into $REC_OUT/$1 (H.264, yuv420p, faststart: plays in QuickTime, browsers, GitHub)
# and write $REC_OUT/markers.json: {"duration": s, "marks": {name: s}} in video seconds
render() {
  echo "file '$(printf "%s/%04d.png" $F $n)'" >> $L       # concat needs the last file twice; -t trims the extra hold
  ffmpeg -v error -y -f concat -safe 0 -i $L -t $(( nf * 1.0 / REC_R )) -vf "fps=$REC_R,scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p" \
    -c:v libx264 -preset slow -crf 20 -movflags +faststart $REC_OUT/$1
  ffprobe -v error -show_entries stream=width,height,codec_name,pix_fmt -show_entries format=duration -of compact $REC_OUT/$1
  local m=""; for k v in ${(kv)MARKS}; do m+="\"$k\": $v, "; done
  printf '{"video": "%s", "duration": %.3f, "marks": {%s}}\n' $1 $(( nf * 1.0 / REC_R )) "${m%, }" > $REC_OUT/markers.json
  echo "markers: $(cat $REC_OUT/markers.json)"
  agent-browser close >/dev/null 2>&1 || true
}
