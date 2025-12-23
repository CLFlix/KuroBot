import Link from "next/link";

function Home() {
  return (
    <>
      <main className="mt-3 mx-5">
        <div className="flex flex-col text-center items-center">
          <h1 className="font-bold text-3xl">
            A lightweight <span className="text-purple-500">Twitch</span> bot
            for <span className="text-pink-400">osu! </span>
            streamers!
          </h1>
          <p className="text-xl max-w-[60%]">
            This locally hosted bot is built to last, taking up very few
            resources so you can enjoy streaming without having to think about
            your PC even slowing down because of it!
          </p>
        </div>
        <div className="flex flex-wrap gap-4 text-xl my-5 justify-center text-white font-bold">
          <span className="bg-gradient-to-r from-violet-600 to-purple-800 hover:bg-purple-500 rounded-lg p-1 hover:scale-103 duration-300">
            <Link href="/commands">View commands</Link>
          </span>
          <span className="bg-gradient-to-r from-red-500 to-pink-700 hover:bg-pink-400 rounded-lg p-1 hover:scale-103 duration-300">
            <Link href="/about">About the bot</Link>
          </span>
          <span className="bg-gradient-to-r from-cyan-700 to-sky-600 hover:bg-blue-400 rounded-lg p-1 hover:scale-103 duration-300">
            <Link href="https://discord.gg/4HAbQm2tdp">Join the Discord!</Link>
          </span>
        </div>
        <div className="flex max-2xl:grid max-2xl:grid-cols-2 gap-10 justify-center">
          <div className="text-block-gradient rounded-lg p-1 text-center border border-black max-w-[14%]">
            <h1 className="text-2xl font-bold">Points System</h1>
            <p className="text-xl">
              Viewers can earn points by sending messages in chat! Points are
              given based on the length of the message, coming with a spam
              protection!
            </p>
          </div>
          <div className="text-block-gradient rounded-lg p-1 text-center border border-black max-w-[14%]">
            <h1 className="text-2xl font-bold">osu! Commands</h1>
            <p className="text-xl">
              Your typical osu! commands are also included! Well-known ones like{" "}
              <code>!np</code> and <code>!nppp</code>, but there's also{" "}
              <code>!rank</code>, <code>!osustats</code> and some more (to
              come)!
            </p>
          </div>
          <div className="text-block-gradient rounded-lg p-1 text-center border border-black max-w-[14%]">
            <h1 className="text-2xl font-bold">Rewards</h1>
            <p className="text-xl">
              Viewers can claim rewards by spending their points to make the
              streamer end the session with a specific map or having them put a
              silly effect over their camera!
            </p>
          </div>
          <div className="text-block-gradient rounded-lg p-1 text-center border border-black max-w-[14%]">
            <h1 className="text-2xl font-bold">Affiliates / Partners</h1>
            <p className="text-xl">
              If you're a Twitch Affiliate or Partner, you can use this bot to
              create 2-minute polls on your channel, as well as having the bot
              listen to channel point redemptions!
            </p>
          </div>
        </div>
        <div className="mt-4 mx-90 text-center grid grid-cols-2 justify-items-center items-center">
          <div className="max-w-[65%]">
            <h1 className="text-3xl font-bold">Open-Source</h1>
            <p className="text-lg">
              This project is completely open-source! The{" "}
              <a href="https://github.com/CLFlix/KuroBot" className="link">
                GitHub repo
              </a>{" "}
              can be found right here! You can help develop this bot or leave
              suggestions in the{" "}
              <a
                href="http://github.com/CLFlix/KuroBot/discussions/categories/suggestions"
                className="link"
              >
                Discussions page
              </a>
              !
            </p>
          </div>
          <div className="max-w-[65%]">
            <h1 className="text-3xl font-bold">Quick Setup</h1>
            <p className="text-lg">
              Download the bot,{" "}
              <a
                href="https://github.com/CLFlix/KuroBot/blob/main/README.md#account-and-authorization"
                className="link"
              >
                get the codes
              </a>
              , run the token scripts and use KuroBot in your Twitch chat!
            </p>
          </div>
        </div>
      </main>
    </>
  );
}

export default Home;
