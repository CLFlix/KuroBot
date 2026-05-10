"use client";

import { useEffect, useState } from "react";
import { useCountdownTimer } from "use-countdown-timer";

type Props = {
  name: string;
  duration: number;
};

const CountDownTimer: React.FC<Props> = ({ name, duration }: Props) => {
  const [timerName, setTimerName] = useState<string>("");

  const { countdown, start, reset, pause, isRunning } = useCountdownTimer({
    timer: 1000 * duration,
  });

  useEffect(() => {
    setTimerName(name);
  }, []);

  function formatTime(countdownTime: number) {
    const minutes = Math.floor(countdownTime / 1000 / 60);
    const seconds = ("0" + Math.floor((countdownTime / 1000) % 60)).slice(-2);

    return `${minutes}:${seconds}`;
  }

  return (
    <div className="countDownTimer">
      <h3 className="timerName">{timerName}</h3>
      <div className="timeLeft">{formatTime(countdown)}</div>
      <button className="timerResetButton" onClick={reset}>
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
    </div>
  );
};

export default CountDownTimer;
