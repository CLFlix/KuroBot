"use client";

import CountDownTimer from "@/components/countDownTimer";
import { StatusMessage } from "@/types";
import { useEffect, useState } from "react";

type UpdateInfo = {
  update: boolean;
  latest: string;
  release_url: string;
};

const Dashboard = () => {
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [takeRequests, setTakeRequests] = useState<boolean>(false);
  const [titleUpdaterOn, setTitleUpdaterOn] = useState<boolean>(false);
  const [listenerOn, setListenerOn] = useState<boolean>(false);
  const [rank, setRank] = useState<number | null>(null);
  const [title, setTitle] = useState<string>("");
  const [points, setPoints] = useState<Record<string, number>>();
  const [top5, setTop5] = useState<[string, number][]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [statusMessages, setStatusMessages] = useState<StatusMessage[]>([]);
  const [stopping, setStopping] = useState<boolean>(false);
  const [updateAvailable, setUpdateAvailable] = useState<UpdateInfo | null>(
    null,
  );

  const baseUrl = "http://localhost:7273";

  const timers = [
    { name: "shush", duration: 300 },
    { name: "memecam", duration: 600 },
    { name: "zoom", duration: 600 },
    { name: "invert", duration: 600 },
  ];
  const remainder = timers.length % 3;
  const fullRows = timers.slice(0, timers.length - (remainder || 0));
  const lastRow = remainder ? timers.slice(-remainder) : [];

  const getTitleUpdaterStatus = async () => {
    if (!isRunning) return;

    const res = await fetch("/titleUpdaterOn");

    if (!res.ok) {
      setTitleUpdaterOn(false);
      return;
    }

    const data = await res.json();
    setTitleUpdaterOn(data);
  };

  const getTakesRequests = async () => {
    if (!isRunning) return;

    const res = await fetch("/takeRequests");

    if (!res.ok) throw new Error("Couldn't get requests status");

    const data = await res.json();
    setTakeRequests(data === true);
  };

  const toggleRequests = async () => {
    const res = await fetch("/toggleRequests", {
      method: "POST",
    });

    if (!res.ok) throw new Error("Could not toggle requests status.");
    setTakeRequests(!takeRequests);
  };

  const getTitle = async () => {
    if (!isRunning) return;

    const res = await fetch(`${baseUrl}/twitchTitle`);

    if (!res.ok) {
      setStatusMessages([
        {
          message: "Could not get current Twitch title",
          type: "error",
        },
      ]);
      return;
    }

    const data = await res.json();
    setTitle(data);
  };

  const getRedemptionsListenerStatus = async () => {
    if (!isRunning) return;

    const res = await fetch("/listener");

    if (!res.ok) {
      setListenerOn(false);
      return;
    }

    const data = await res.json();
    setListenerOn(data === true);
  };

  const getRank = async () => {
    if (!isRunning) return;

    const res = await fetch("/rank");

    if (!res.ok) throw new Error("Could not get current osu! rank.");

    const data = await res.json();
    setRank(data);
  };

  const updateTitle = async () => {
    setLoading(true);
    setStatusMessages([]);

    if (!isRunning) {
      setStatusMessages([{ message: "Bot is not running...", type: "error" }]);
      return;
    }

    const response = await fetch("/update_title");

    if (!response.ok) {
      setStatusMessages([
        {
          message: "Could not update title right now...",
          type: "error",
        },
      ]);
      setLoading(false);
      return;
    }
    setStatusMessages([
      {
        message: "Updated title",
        type: "success",
      },
    ]);
    setLoading(false);
    getTitle();
  };

  const getPoints = async () => {
    if (!isRunning) return;

    const res = await fetch(`${baseUrl}/points`);

    if (!res.ok) throw new Error("Could not get points.");

    const data = await res.json();
    setPoints(data);
    sortPoints(data);
  };

  const sortPoints = (data: Record<string, number>) => {
    const top_users = Object.entries(data)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 5);
    setTop5(top_users);
  };

  const stopBot = async () => {
    setStopping(true);
    const res = await fetch("/stop", {
      method: "POST",
    });
    if (!res.ok) throw new Error("Couldn't request bot shutdown...");
    return;
  };

  const getIsRunning = async () => {
    await fetch(`${baseUrl}/isRunning`)
      .then((data) => {
        data.json().then((hello) => setIsRunning(hello === "hello"));
      })
      .catch(() => {
        setIsRunning(false);
        setStopping(false);
      });
  };

  const getUpdateStatus = async () => {
    await fetch("/updateStatus")
      .then((data) => {
        data.json().then((data) => setUpdateAvailable(data));
      })
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    getIsRunning();

    const interval = setInterval(getIsRunning, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    getTitleUpdaterStatus();
    getRedemptionsListenerStatus();

    setTimeout(getUpdateStatus, 1000);
  }, [isRunning]);

  useEffect(() => {
    getRank();
    getTitle();
    getTakesRequests();

    const current_rank = setInterval(getRank, 60000); // change to something lower for dev
    const current_title = setInterval(getTitle, 60000);

    return () => {
      clearInterval(current_rank);
      clearInterval(current_title);
    };
  }, [isRunning]);

  useEffect(() => {
    getPoints();

    const bot_points = setInterval(getPoints, 10000); // change to something lower for dev

    return () => clearInterval(bot_points);
  }, [isRunning]);

  useEffect(() => {
    if (statusMessages.length === 0) return;

    const timer = setTimeout(() => {
      setStatusMessages([]);
    }, 3000);

    return () => clearTimeout(timer);
  }, [statusMessages]);

  return (
    <main className="mt-4 mx-4">
      <h1 className="text-3xl font-bold text-center">KuroBot Dashboard</h1>
      <div className="grid grid-cols-3">
        <div className="flex flex-col">
          {isRunning && (
            <>
              <h2 className="text-2xl font-bold mt-2">Title Updates</h2>
              <table className="streamTitleTable mt-1">
                <thead>
                  <tr className="text-2xl text-center">
                    <td className="px-3">osu! Rank</td>
                    <td className="px-3">Current Stream Title</td>
                  </tr>
                </thead>
                <tbody>
                  <tr className="text-center">
                    <td className="px-3">{rank}</td>
                    <td className="px-3">{title}</td>
                  </tr>
                </tbody>
              </table>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => updateTitle()}
                  className="mt-3 discord-button"
                  disabled={loading}
                >
                  Update Stream Title
                </button>
                {statusMessages.length > 0 && (
                  <p
                    className={
                      statusMessages[0].type === "success"
                        ? "text-green-400 mt-3"
                        : "text-red-500 mt-3"
                    }
                  >
                    {statusMessages[0].message}
                  </p>
                )}
              </div>
              <div className="mt-4">
                <p className="text-xl">
                  <span className="font-bold">Automatic title updater:</span>{" "}
                  <span
                    className={
                      titleUpdaterOn ? "text-green-400" : "text-red-500"
                    }
                  >
                    {titleUpdaterOn ? "On" : "Off"}
                  </span>
                </p>
              </div>
              <div>
                <p className="text-xl">
                  <span className="font-bold">
                    Twitch Redemptions Listener:
                  </span>{" "}
                  <span
                    className={listenerOn ? "text-green-400" : "text-red-500"}
                  >
                    {listenerOn ? "On" : "Off"}
                  </span>
                </p>
              </div>
            </>
          )}
        </div>

        <div className="flex flex-col text-center">
          <div>
            <h2 className="text-2xl font-bold mt-2">Bot status</h2>
            <div>
              <p
                className={
                  isRunning ? "text-xl text-green-400" : "text-xl text-red-500"
                }
              >
                {isRunning ? (
                  stopping ? (
                    <p className="text-red-400">
                      Stopping bot, this might take a minute...
                    </p>
                  ) : (
                    <p className="text-green-500">Running...</p>
                  )
                ) : (
                  <div>
                    <p>Not running...</p>
                    <p className="text-white">
                      If you are running the bot and looking at the website
                      hosted by GitHub, go to{" "}
                      <a
                        href="http://localhost:7273"
                        className="link"
                        target="_blank"
                      >
                        the locally hosted page
                      </a>{" "}
                      to view the working Dashboard.
                    </p>
                  </div>
                )}
              </p>
            </div>
            {isRunning &&
              (stopping ? (
                <></>
              ) : (
                <button className="stop-button mt-2 text-lg" onClick={stopBot}>
                  Stop bot
                </button>
              ))}
          </div>

          {isRunning && (
            <div>
              <div>
                <h2 className="text-2xl font-bold mt-4">Taking requests?</h2>
                <p
                  className={`text-xl ${
                    takeRequests ? "text-green-400" : "text-red-400"
                  }`}
                >
                  {takeRequests ? "Yes" : "No"}
                </p>
              </div>
              <button
                className="discord-button mt-2 text-lg"
                onClick={toggleRequests}
              >
                {takeRequests
                  ? "Stop taking requests"
                  : "Start taking requests"}
              </button>
              {updateAvailable?.update && (
                <div className="text-lg mt-4">
                  <p>
                    KuroBot has a fancypancy update! Download KuroBot v
                    {updateAvailable.latest} over at
                  </p>
                  <a
                    href={updateAvailable.release_url}
                    className="link"
                    target="_blank"
                  >
                    {updateAvailable.release_url}
                  </a>
                  !
                </div>
              )}
            </div>
          )}
        </div>

        {isRunning && (
          <div>
            {points && (
              <div>
                <h2 className="text-xl font-bold mt-2">Top 5 Points Owners:</h2>
                <table className="pointsTable mt-3">
                  <thead>
                    <tr className="text-center text-2xl">
                      <td className="px-3">Username</td>
                      <td className="px-3">Amount</td>
                    </tr>
                  </thead>
                  <tbody>
                    {top5.map((user, index) => (
                      <tr key={index}>
                        <td className="px-2 py-1">{user[0]}</td>
                        <td className="px-2 py-1 text-center">{user[1]}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>

      {isRunning && (
        <div className="mt-4 w-[55%] grid grid-cols-3 content-center mx-auto">
          {fullRows.map((t) => (
            <CountDownTimer key={t.name} name={t.name} duration={t.duration} />
          ))}
          {lastRow.length > 0 && (
            <div className="col-span-3 flex justify-center gap-x-30">
              {lastRow.map((t) => (
                <CountDownTimer
                  key={t.name}
                  name={t.name}
                  duration={t.duration}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </main>
  );
};

export default Dashboard;
