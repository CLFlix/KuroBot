"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const initializeBot = () => {
  const router = useRouter();

  const [rq, setRq] = useState<boolean>(false);
  const [affiliate, setAffiliate] = useState<boolean>(false);
  const [update, setUpdate] = useState<boolean>(false);
  const [initStatus, setInitStatus] = useState<boolean>(false);

  useEffect(() => {
    if (initStatus) return;

    const getInitializedStatus = async () => {
      await fetch("/initStatus").then((data) =>
        data
          .json()
          .then((status) => setInitStatus(status))
          .catch((err) => console.error(err)),
      );
    };

    getInitializedStatus();
  }, [initStatus]);

  const startupBot = async (
    rq: boolean,
    affiliate: boolean,
    update: boolean,
  ) => {
    const res = await fetch("/initialize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rq, affiliate, update }),
    });
    if (!res.ok) throw new Error("Something went wrong starting up the bot...");

    router.push("http://localhost:7273/");
  };

  return (
    <main className="m-4 flex justify-center">
      <div>
        {initStatus ? (
          <div className="text-xl">
            <Link href="http://localhost:7273/" className="link">
              Go to the dashboard..
            </Link>
          </div>
        ) : (
          <form className="text-lg">
            <div>
              <label htmlFor="rq_selection">
                Do you want to take map requests during the stream?
              </label>
              <select
                name="rq_selection"
                onChange={(e) => setRq(e.target.value === "requests_yes")}
              >
                <option value="requests_no">No</option>
                <option value="requests_yes">Yes</option>
              </select>
            </div>
            <div>
              <label htmlFor="affiliate_selection">
                Are you a Twitch Affiliate / Partner?
              </label>
              <select
                name="affiliate_selection"
                onChange={(e) =>
                  setAffiliate(e.target.value === "affiliate_yes")
                }
              >
                <option value="affiliate_no">No</option>
                <option value="affiliate_yes">Yes</option>
              </select>
            </div>
            <div>
              <label htmlFor="update_selection">
                Do you want your rank to be automatically updated in your title?
              </label>
              <select
                name="update_selection"
                onChange={(e) => setUpdate(e.target.value === "update_yes")}
              >
                <option value="update_no">No</option>
                <option value="update_yes">Yes</option>
              </select>
            </div>
            <div className="flex justify-center">
              <button
                className="discord-button mt-2"
                onClick={(e) => {
                  e.preventDefault();
                  startupBot(rq, affiliate, update);
                }}
              >
                Start bot
              </button>
            </div>
          </form>
        )}
      </div>
    </main>
  );
};

export default initializeBot;
