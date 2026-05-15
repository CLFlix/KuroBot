"use client";

import { useEffect, useState } from "react";
import { useCountdownTimer } from "use-countdown-timer";

type Props = {
  name: string;
  duration: number;
};

const CountDownTimer: React.FC<Props> = ({ name, duration }: Props) => {
  const [timerName, setTimerName] = useState<string>("");
  const [timerDuration, setTimerDuration] = useState<number>(1000 * duration);

  const bell = new Audio("/static/audio/softBellSound.mp3");
  bell.volume = 0.3;

  const { countdown, start, reset, pause, isRunning } = useCountdownTimer({
    timer: timerDuration,
  });

  useEffect(() => {
    setTimerName(name);
  }, []);

  useEffect(() => {
    reset();
  }, [timerDuration]);

  function formatTime(countdownTime: number) {
    const minutes = Math.floor(countdownTime / 1000 / 60);
    const seconds = ("0" + Math.floor((countdownTime / 1000) % 60)).slice(-2);

    return `${minutes}:${seconds}`;
  }

  function changeDuration(delta: number) {
    setTimerDuration((prev) => Math.max(0, prev + delta * 1000));
  }

  function playBellSound() {
    bell.play();
  }

  // play sound when timer ends
  if (isRunning && countdown === 0) {
    playBellSound();
  }

  return (
    <div className="countDownTimer">
      <div className="title">
        <h3 className="timerName capitalize">{timerName}</h3>
        <p className="timeLeft">{formatTime(countdown)}</p>
      </div>
      <div className="buttons">
        <button
          onClick={() => changeDuration(-duration)}
          className="timerDecrease"
        >
          -{formatTime(duration * 1000)}
        </button>
        <button
          className="stop-button"
          onClick={() => {
            setTimerDuration(duration * 1000);
            reset();
          }}
        >
          Reset
        </button>
        {isRunning ? (
          <button className="timerPauseButton" onClick={pause}>
            Pause
          </button>
        ) : (
          <button className="timerStartButton" onClick={start}>
            Start
          </button>
        )}
        <button
          onClick={() => changeDuration(duration)}
          className="timerIncrease"
        >
          +{formatTime(duration * 1000)}
        </button>
      </div>
    </div>
  );
};

export default CountDownTimer;
