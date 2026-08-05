"use client";

import { useChartEngineStore } from "../stores/chart-engine-store";
import { Button } from "@/components/design-system/primitives/button";

export function ReplayControls() {
  const replay = useChartEngineStore((s) => s.replay);
  const setReplayState = useChartEngineStore((s) => s.setReplayState);

  const togglePlay = () => {
    setReplayState({ isPlaying: !replay.isPlaying });
  };

  const stepForward = () => {
    setReplayState({ currentIndex: Math.min(replay.currentIndex + 1, replay.totalCandles - 1) });
  };

  const stepBack = () => {
    setReplayState({ currentIndex: Math.max(replay.currentIndex - 1, 0) });
  };

  const changeSpeed = (delta: number) => {
    const newSpeed = Math.min(Math.max(replay.speed + delta, 1), 16);
    setReplayState({ speed: newSpeed });
  };

  return (
    <div className="flex items-center gap-2">
      <Button variant="secondary" size="sm" onClick={stepBack}>
        ⏮
      </Button>
      <Button variant="primary" size="sm" onClick={togglePlay}>
        {replay.isPlaying ? "⏸" : "▶"}
      </Button>
      <Button variant="secondary" size="sm" onClick={stepForward}>
        ⏭
      </Button>
      <div className="flex items-center gap-1">
        <Button variant="secondary" size="sm" onClick={() => changeSpeed(-1)}>
          -
        </Button>
        <span className="text-xs text-[var(--color-secondary-500)] w-8 text-center">{replay.speed}x</span>
        <Button variant="secondary" size="sm" onClick={() => changeSpeed(1)}>
          +
        </Button>
      </div>
    </div>
  );
}


