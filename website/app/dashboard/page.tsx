"use client";

import { StatusMessage } from "@/types";
import { useEffect, useState } from "react";

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

  const getTitleUpdaterStatus = async () => {
    if (!isRunning) return;

    const res = await fetch("http://localhost:7273/titleUpdaterOn");

    if (!res.ok) {
      setTitleUpdaterOn(false);
      return;
    }

    const data = await res.json();
    setTitleUpdaterOn(data);
  };

  const getTakesRequests = async () => {
    if (!isRunning) return;

    const res = await fetch("http://localhost:7273/takeRequests");

    if (!res.ok) throw new Error("Couldn't get requests status");

    const data = await res.json();
    setTakeRequests(data === true);
  };

  const toggleRequests = async () => {
    const res = await fetch("http://localhost:7273/toggleRequests", {
      method: "POST",
    });

    if (!res.ok) throw new Error("Could not toggle requests status.");

    const data = await res.json();
    setTakeRequests(!takeRequests);
  };

  const getTitle = async () => {
    if (!isRunning) return;

    const res = await fetch("http://localhost:7273/twitchTitle");

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

    const res = await fetch("http://localhost:7273/listener");

    if (!res.ok) {
      setListenerOn(false);
      return;
    }

    const data = await res.json();
    setListenerOn(data === true);
  };

  const getRank = async () => {
    if (!isRunning) return;

    const res = await fetch("http://localhost:7273/rank");

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

    const response = await fetch("http://localhost:7273/update_title");

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
  };

  const getPoints = async () => {
    if (!isRunning) return;

    const res = await fetch("http://localhost:7273/points");

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
    const res = await fetch("http://localhost:7273/stop", {
      method: "POST",
    });
    if (!res.ok) throw new Error("Couldn't request bot shutdown...");
    return;
  };

  useEffect(() => {
    const getIsRunning = async () => {
      await fetch("http://localhost:7273/isRunning")
        .then((data) => {
          data.json().then((hello) => setIsRunning(hello === "hello"));
        })
        .catch(() => setIsRunning(false));
    };
    getIsRunning();

    const interval = setInterval(getIsRunning, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    getTitleUpdaterStatus();
    getRedemptionsListenerStatus();
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
        <div>
          {isRunning && (
            <>
              <h2 className="text-2xl font-bold mt-2">Title Updates</h2>
              <table className="mt-2">
                <thead>
                  <tr className="text-2xl">
                    <td className="table-header-gradient px-3">osu! Rank</td>
                    <td className="table-header-gradient px-3">
                      Current Stream Title
                    </td>
                  </tr>
                </thead>
                <tbody>
                  <tr className="text-center">
                    <td className="table-command-gradient">{rank}</td>
                    <td className="table-command-gradient">{title}</td>
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
                {isRunning ? "Running..." : "Not running..."}
              </p>
            </div>
            {isRunning && (
              <button className="discord-button mt-2 text-lg" onClick={stopBot}>
                Stop bot
              </button>
            )}
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
            </div>
          )}
        </div>

        {isRunning && (
          <div>
            {points && (
              <div>
                <h2 className="text-xl font-bold mt-2">Top 5 Points Owners:</h2>
                <table className="mt-3">
                  <thead>
                    <tr className="text-center text-2xl">
                      <td className="table-header-gradient px-3">Username</td>
                      <td className="table-header-gradient px-3">Amount</td>
                    </tr>
                  </thead>
                  <tbody>
                    {top5.map((user, index) => (
                      <tr key={index}>
                        <td className="px-2 py-1 table-command-gradient">
                          {user[0]}
                        </td>
                        <td className="px-2 py-1 table-command-gradient text-center">
                          {user[1]}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
};

export default Dashboard;
