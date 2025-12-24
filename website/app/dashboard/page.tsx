"use client";

import { StatusMessage } from "@/types";
import { useEffect, useState } from "react";

const Dashboard = () => {
  const [rank, setRank] = useState<number | null>(null);
  const [title, setTitle] = useState<string>("");
  const [points, setPoints] = useState<Record<string, number>>();
  const [top5, setTop5] = useState<[string, number][]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [statusMessages, setStatusMessages] = useState<StatusMessage[]>([]);

  const getTitle = async () => {
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

  const getRank = async () => {
    const res = await fetch("http://localhost:7273/rank");

    if (!res.ok) throw new Error("Could not get current osu! rank.");

    const data = await res.json();
    setRank(data);
  };

  const sortPoints = (data: Record<string, number>) => {
    const top_users = Object.entries(data)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 5);
    setTop5(top_users);
  };

  const getPoints = async () => {
    const res = await fetch("http://localhost:7273/points");

    if (!res.ok) throw new Error("Could not get points.");

    const data = await res.json();
    setPoints(data);
    sortPoints(data);
  };

  useEffect(() => {
    getRank();
    getTitle();
    getPoints();

    const current_rank = setInterval(getRank, 5000); // change to something lower for dev
    const current_title = setInterval(getTitle, 5000); // change to something lower for dev
    const bot_points = setInterval(getPoints, 10000); // change to something lower for dev

    return () => {
      clearInterval(current_rank);
      clearInterval(current_title);
      clearInterval(bot_points);
    };
  }, []);

  const updateTitle = async () => {
    setLoading(true);
    setStatusMessages([]);
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

  useEffect(() => {
    if (statusMessages.length === 0) return;

    const timer = setTimeout(() => {
      setStatusMessages([]);
    }, 3000);

    return () => clearTimeout(timer);
  }, [statusMessages]);

  return (
    <main className="mt-4 ml-4">
      <h1 className="text-3xl font-bold">KuroBot Dashboard</h1>
      <table className="mt-2">
        <thead>
          <tr className="text-2xl">
            <td className="table-header-gradient px-3">osu! Rank</td>
            <td className="table-header-gradient px-3">Current Stream Title</td>
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

      {points && (
        <div>
          <h2 className="text-xl font-bold mt-5">Top 5 Points Owners:</h2>
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
    </main>
  );
};

export default Dashboard;
