---
name: record-it
description: Record a demo video of a web app flow, a user driving the running app with a visible cursor, click ripples and captions, rendered to a Full HD MP4. Uses agent-browser screenshots stitched with ffmpeg. Use when the user wants a screen recording, demo video, walkthrough video, or "record the flow" for a PR, a client, or docs. To just confirm a flow works, use prove-it.
allowed-tools: Bash, Read, Write, Edit
---

# record-it

Make a short, readable MP4 of a flow in the **running app**. The video is a sequence of headless screenshots, each held for a set time, stitched by ffmpeg. A fake cursor is drawn into the page, because headless screenshots never show the real mouse.

## Why screenshots, not native recording

`agent-browser record start/stop` exists but proved unreliable: 10 fps WebM, dropped whole parts of the flow (the start, or the second half), and squashed long holds. Screenshots with explicit hold times give full control over pacing and never lose a step. Use native recording only if the user asks for it and check the result frame by frame.

## Flow

1. **Storyboard.** Write the steps as a short list: who logs in, what gets clicked, which states to hold. Agree it with the user if the flow isn't obvious. Aim for 30-60 s.
2. **Selectors.** Read the page code for stable ids and data attributes. Test each one with `agent-browser eval` before recording.
3. **Script.** Copy `scripts/example.zsh`, edit the steps. It sources `scripts/lib.zsh`, which gives you:

   | Helper | Does |
   |---|---|
   | `start URL` / `go URL` | set the 1920x1080 viewport, open a page, restore the overlay |
   | `shot SECS` | one frame, held for SECS |
   | `glide SEL [dx]` | eased cursor move to an element (6-12 frames at 0.04 s) |
   | `click SEL` | glide, ripple, then a JS click. `SEL@2` picks the third match |
   | `scrollto SEL [offset]` | eased scroll until SEL's top is `offset` px below the viewport top (default 120). Finds the element's own scroll container, so pages that scroll inside a `<main>` work |
   | `mark NAME` | note the current video time under NAME; `render` writes all marks to `markers.json` |
   | `typeslow SEL TEXT` | click into a field, type one character per frame (0.13 s) |
   | `choose SEL VALUE` | click a `<select>`, then set its value |
   | `caption TEXT` | dark pill at top-center; `caption ""` hides it |
   | `until_js COND` | wait for a condition, then restore the overlay (use after any reload) |
   | `render NAME.mp4` | stitch to H.264, yuv420p, 30 fps, faststart; prints ffprobe; writes `markers.json` |

4. **Run.** `zsh storyboard.zsh <out-dir>`. Output goes to the session scratchpad, never the repo.
5. **Verify.** Check the ffprobe line (1920x1080, h264, yuv420p), and that its duration equals `duration` in `markers.json`. Extract 3-5 frames with `ffmpeg -ss <t> -i video.mp4 -frames:v 1 f.png` (one mid-glide, one per key state, one with a caption) and look at them. Compare the counts and names you logged during the run with what the frames show.
6. **Deliver.** Give the path and the `open` command. The user reviews it before it goes anywhere.

## Phone viewport

Set `REC_W=402 REC_H=874 REC_SCALE=2` before sourcing the lib. `start` applies the device scale, so frames come out 804x1748 and stay sharp when scaled into a phone frame. Below 700 px wide the lib switches to a round tap dot instead of the arrow, and `caption` does nothing, because the pill does not fit. Put the text next to the phone in the edit instead. Override with `REC_TOUCH=0` or `REC_CAPTIONS=1`.

## Feeding HyperFrames

Each hold is rounded to whole video frames, so a `mark` time is exact to the frame in the MP4. Call `mark` just before the step it names (`mark part2` before the first frame of part 2, `mark tap` before the click whose result you want to cue on). `markers.json` looks like:

```json
{"video": "desktop.mp4", "duration": 43.867, "marks": {"part2": 31.6, "tap": 4.9}}
```

Use the marks in the composition: `data-media-start` to cut one recording into parts, and `data-start` offsets to cue slides, captions or checklists on what happens in the clip. With `data-playback-rate`, divide the mark by the rate. Record one MP4 per viewport (desktop, phone) and put each in its own frame in the composition.

## Pacing that reads well

- Hold key states 2-3.5 s, the first frame about 2.5 s, transitions 0.3-0.6 s.
- Caption at the start of each actor's part ("Barbara, Coordinator of Wandsbek").
- There is no address bar in the frames. When the URL matters, show it as a caption.

## Gotchas

- **Clicks under sticky headers.** agent-browser may report an element as "covered", or click and silently do nothing. `click` draws the cursor, then clicks via JS. Pressing Enter to submit a form was unreliable too; click the submit button.
- **Leftover state.** A failed earlier run can leave you logged in. Reset the state at the start and assert it before the first frame (see `example.zsh`).
- **Reloads wipe the overlay.** Login and logout reload the page. Always follow them with `until_js` or `go`, which re-inject the cursor at its last position.
- **Native `<select>` lists** never render in headless screenshots. Show the focus and the new value, or add a caption.
- **zsh doesn't word-split** `$AB` style command variables. Use functions, as `lib.zsh` does.
- **`VAR=x source lib.zsh`** only sets VAR for the source itself. The lib saves what it needs at load time.
- **Don't change data** unless the storyboard needs it. Use a separate `REC_SESSION` and let `render` close it.

## Delivering to GitHub

GitHub has no API for attaching a video to a PR or issue. Give the user the MP4 path to drag into the comment box. Don't convert to GIF unless asked, and don't commit videos to git.
