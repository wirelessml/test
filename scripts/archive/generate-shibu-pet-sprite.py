#!/usr/bin/env python3
"""Generate a Codex Pet spritesheet for "ミニマリストしぶ" (Minimalist Shibu).

Layout: 8 cols x 9 rows of 192x208 frames -> 1536x1872 webp.
Each row corresponds to an animation (row index = animation):
  0 idle, 1 run-right, 2 run-left, 3 wave, 4 jump, 5 fail, 6 wait, 7 run, 8 review

Style: black silhouette stick-figure minimalist on transparent BG.
Suggests "shibu = monochrome, lean, no possessions" without using a real likeness.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

# Spec
FRAME_W, FRAME_H = 192, 208
COLS, ROWS = 8, 9
SHEET_W, SHEET_H = FRAME_W * COLS, FRAME_H * ROWS

BLACK = (32, 32, 32, 255)
HIGHLIGHT = (160, 160, 160, 255)
TRANSPARENT = (0, 0, 0, 0)

# Body proportions (relative to frame)
HEAD_R = 18  # head radius
TORSO_LEN = 60
LIMB_LEN = 42
BASE_X = FRAME_W // 2
BASE_Y_FOOT = FRAME_H - 24  # foot baseline


def draw_figure(draw: ImageDraw.ImageDraw, cx: int, cy_foot: int,
                 left_arm_angle: float, right_arm_angle: float,
                 left_leg_angle: float, right_leg_angle: float,
                 lean: float = 0.0,
                 head_dy: int = 0,
                 facing_left: bool = False) -> None:
    """Draw one stick-figure pose. Angles in radians, 0 = pointing down."""
    # vertical body axis with optional lean
    hip_x = cx + int(lean * 8)
    hip_y = cy_foot - LIMB_LEN
    shoulder_x = hip_x + int(lean * 6)
    shoulder_y = hip_y - TORSO_LEN
    head_cx = shoulder_x + int(lean * 4)
    head_cy = shoulder_y - HEAD_R - 4 + head_dy

    # Mirror angles when facing left
    if facing_left:
        left_arm_angle = math.pi - left_arm_angle
        right_arm_angle = math.pi - right_arm_angle
        left_leg_angle = math.pi - left_leg_angle
        right_leg_angle = math.pi - right_leg_angle

    # Limb endpoints
    def pt(origin_x: int, origin_y: int, angle: float, length: int) -> tuple[int, int]:
        return (origin_x + int(math.sin(angle) * length),
                origin_y + int(math.cos(angle) * length))

    larm_end = pt(shoulder_x, shoulder_y, left_arm_angle, LIMB_LEN)
    rarm_end = pt(shoulder_x, shoulder_y, right_arm_angle, LIMB_LEN)
    lleg_end = pt(hip_x, hip_y, left_leg_angle, LIMB_LEN)
    rleg_end = pt(hip_x, hip_y, right_leg_angle, LIMB_LEN)

    # Head (circle)
    draw.ellipse(
        (head_cx - HEAD_R, head_cy - HEAD_R, head_cx + HEAD_R, head_cy + HEAD_R),
        fill=BLACK,
    )
    # Torso
    draw.line((shoulder_x, shoulder_y, hip_x, hip_y), fill=BLACK, width=8)
    # Arms
    draw.line((shoulder_x, shoulder_y, *larm_end), fill=BLACK, width=7)
    draw.line((shoulder_x, shoulder_y, *rarm_end), fill=BLACK, width=7)
    # Legs
    draw.line((hip_x, hip_y, *lleg_end), fill=BLACK, width=8)
    draw.line((hip_x, hip_y, *rleg_end), fill=BLACK, width=8)


# Angle convention (in pt()): 0 = straight down, +π/2 = right, -π/2 = left, π = up.
# So arms slightly out from torso = ±0.4 rad. Legs nearly straight = ±0.15.

def frame_idle(idx: int, draw: ImageDraw.ImageDraw, cx: int) -> None:
    """Idle: subtle breathing, arms relaxed, slight bob (idx 0..7)."""
    bob = int(2 * math.sin(idx * math.pi / 4))
    draw_figure(
        draw, cx, BASE_Y_FOOT + bob,
        left_arm_angle=-0.45,
        right_arm_angle=0.45,
        left_leg_angle=-0.18,
        right_leg_angle=0.18,
        head_dy=-bob,
    )


def frame_run(idx: int, draw: ImageDraw.ImageDraw, cx: int, facing_left: bool) -> None:
    """Run cycle: alternating arms/legs."""
    swing = math.sin(idx * math.pi / 4) * 0.9
    bounce = abs(math.sin(idx * math.pi / 4)) * 4
    draw_figure(
        draw, cx, BASE_Y_FOOT - int(bounce),
        left_arm_angle=-0.6 - swing,
        right_arm_angle=0.6 + swing,
        left_leg_angle=-0.35 + swing,
        right_leg_angle=0.35 - swing,
        lean=0.5 if not facing_left else -0.5,
        facing_left=facing_left,
    )


def frame_wave(idx: int, draw: ImageDraw.ImageDraw, cx: int) -> None:
    """Wave: right arm raised up, hand swinging side-to-side."""
    swing = math.sin(idx * math.pi / 2) * 0.35
    draw_figure(
        draw, cx, BASE_Y_FOOT,
        left_arm_angle=-0.4,
        right_arm_angle=math.pi - 0.6 + swing,  # raised up (close to π = pointing up)
        left_leg_angle=-0.18,
        right_leg_angle=0.18,
    )


def frame_jump(idx: int, draw: ImageDraw.ImageDraw, cx: int) -> None:
    """Jump: 5 frames - crouch, leap, peak, descent, land."""
    poses = [
        (0, -0.6, 0.6, -0.6, 0.6),       # crouch (legs bent wide)
        (-12, -1.0, 1.0, -0.4, 0.4),     # take-off (arms swing up, legs straighten)
        (-32, math.pi - 0.7, -(math.pi - 0.7), -0.25, 0.25),  # peak (arms up, legs down)
        (-12, -1.0, 1.0, -0.4, 0.4),     # descent
        (0, -0.5, 0.5, -0.4, 0.4),       # land
    ]
    dy, larm, rarm, lleg, rleg = poses[min(idx, 4)]
    draw_figure(
        draw, cx, BASE_Y_FOOT + dy,
        left_arm_angle=larm, right_arm_angle=rarm,
        left_leg_angle=lleg, right_leg_angle=rleg,
    )


def frame_fail(idx: int, draw: ImageDraw.ImageDraw, cx: int) -> None:
    """Failed: drooping shoulders, head down, lean forward."""
    droop = min(idx, 7) / 7.0
    head_dy = int(droop * 10)
    arm_droop = -0.15 - droop * 0.1
    draw_figure(
        draw, cx, BASE_Y_FOOT,
        left_arm_angle=arm_droop, right_arm_angle=-arm_droop,
        left_leg_angle=-0.15, right_leg_angle=0.15,
        head_dy=head_dy, lean=droop * 0.3,
    )


def frame_wait(idx: int, draw: ImageDraw.ImageDraw, cx: int) -> None:
    """Waiting: tap foot, casual stance (6 frames)."""
    tap = math.sin(idx * math.pi / 3) * 0.4
    draw_figure(
        draw, cx, BASE_Y_FOOT,
        left_arm_angle=-0.35, right_arm_angle=0.35,
        left_leg_angle=-0.12, right_leg_angle=0.18 + tap,
    )


def frame_run_idle(idx: int, draw: ImageDraw.ImageDraw, cx: int) -> None:
    """Running (slow, in-place, 6 frames)."""
    swing = math.sin(idx * math.pi / 3) * 0.7
    draw_figure(
        draw, cx, BASE_Y_FOOT - int(abs(swing) * 4),
        left_arm_angle=-0.5 - swing,
        right_arm_angle=0.5 + swing,
        left_leg_angle=-0.3 + swing,
        right_leg_angle=0.3 - swing,
    )


def frame_review(idx: int, draw: ImageDraw.ImageDraw, cx: int) -> None:
    """Review: hand on chin, head tilted (6 frames)."""
    tilt = math.sin(idx * math.pi / 3) * 0.18
    draw_figure(
        draw, cx, BASE_Y_FOOT,
        left_arm_angle=-0.4,
        right_arm_angle=math.pi - 0.9,  # arm bent up to chin
        left_leg_angle=-0.18, right_leg_angle=0.18,
        lean=tilt,
    )


def build_spritesheet(out_path: Path) -> None:
    sheet = Image.new("RGBA", (SHEET_W, SHEET_H), TRANSPARENT)

    rows = [
        # row 0: idle (8 frames, full row)
        ("idle", 8, frame_idle),
        # row 1: run-right (8 frames)
        ("run-right", 8, lambda i, d, cx: frame_run(i, d, cx, facing_left=False)),
        # row 2: run-left (8 frames)
        ("run-left", 8, lambda i, d, cx: frame_run(i, d, cx, facing_left=True)),
        # row 3: wave (4 frames + 4 padding)
        ("wave", 4, frame_wave),
        # row 4: jump (5 frames + 3 padding)
        ("jump", 5, frame_jump),
        # row 5: fail (8 frames)
        ("fail", 8, frame_fail),
        # row 6: wait (6 frames + 2 padding)
        ("wait", 6, frame_wait),
        # row 7: running (6 frames + 2 padding)
        ("running", 6, frame_run_idle),
        # row 8: review (6 frames + 2 padding)
        ("review", 6, frame_review),
    ]

    for row_idx, (name, count, drawer) in enumerate(rows):
        for col in range(COLS):
            frame = Image.new("RGBA", (FRAME_W, FRAME_H), TRANSPARENT)
            draw = ImageDraw.Draw(frame)
            # Use first frame as fallback for padding columns
            effective_idx = col if col < count else 0
            drawer(effective_idx, draw, FRAME_W // 2)
            sheet.paste(frame, (col * FRAME_W, row_idx * FRAME_H), frame)

    # Save as webp (lossless to keep silhouette crisp)
    sheet.save(out_path, format="WEBP", lossless=True, quality=100, method=6)
    print(f"Wrote {out_path} ({SHEET_W}x{SHEET_H})")


if __name__ == "__main__":
    out = Path.home() / ".codex" / "pets" / "shibu" / "spritesheet.webp"
    out.parent.mkdir(parents=True, exist_ok=True)
    build_spritesheet(out)
