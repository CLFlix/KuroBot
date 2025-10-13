import Footer from "@/components/Footer";
import Header from "@/components/Header";
import Link from "next/link";

function Home() {
  return (
    <>
      <Header />
      <main className="mt-3 ml-5 mr-5 font-sans">
        <section className="flex flex-col text-center font-sans">
          <h1 className="font-bold text-3xl">
            A lightweight <span className="text-purple-500">Twitch</span> bot
            for <span className="text-pink-400">osu! </span>
            streamers!
          </h1>
          <p className="text-xl">
            This locally hosted bot is built to last, taking up very few
            resources so you can enjoy streaming without having to think about
            your PC crashing because of it!
          </p>
        </section>
        <section className="flex flex-wrap gap-4 text-xl mt-5 justify-center text-white font-semibold">
          <span className="bg-gradient-to-r from-purple-600 via-purple-700 to-purple-800 hover:bg-purple-500 rounded-lg p-1">
            <Link href="/commands">View commands</Link>
          </span>
          <span className="bg-gradient-to-r from-pink-500 via-pink-600 to-pink-700 hover:bg-pink-400 rounded-lg p-1">
            <Link href="/about">About the bot</Link>
          </span>
          <span className="bg-gradient-to-r from-blue-700 via-blue-800 to-blue-900 hover:bg-blue-400 rounded-lg p-1">
            <a href="https://discord.gg/4HAbQm2tdp">Join the Discord!</a>
          </span>
        </section>
        <section className="flex max-2xl:grid max-2xl:grid-cols-2 gap-10 justify-center mt-5">
          <div className="bg-gradient-to-br from-gray-800 to-gray-500 rounded-lg p-1 text-center">
            <h1 className="text-2xl font-bold">Points System</h1>
            <p className="text-xl max-w-[270px] max-2xl:max-w-[500px]">
              Viewers can earn points by sending messages in chat! Points are
              given based on the length of the message, coming with a spam
              protection!
            </p>
          </div>
          <div className="bg-gradient-to-br from-gray-800 to-gray-500 rounded-lg p-1 text-center">
            <h1 className="text-2xl font-bold">osu! Commands</h1>
            <p className="text-xl max-w-[270px] max-2xl:max-w-[500px]">
              Your typical osu! commands are also included! Well-known ones like{" "}
              <code>?np</code> and <code>?nppp</code>, but there's also{" "}
              <code>?rank</code>, <code>osustats</code> and some more (to come)!
            </p>
          </div>
          <div className="bg-gradient-to-br from-gray-800 to-gray-500 rounded-lg p-1 text-center">
            <h1 className="text-2xl font-bold">Rewards</h1>
            <p className="text-xl max-w-[270px] max-2xl:max-w-[500px]">
              Viewers can claim rewards by spending their points to make the
              streamer end the session with a specific map or having them put a
              silly effect over their camera!
            </p>
          </div>
          <div className="bg-gradient-to-br from-gray-800 to-gray-500 rounded-lg p-1 text-center">
            <h1 className="text-2xl font-bold">Affiliates / Partners</h1>
            <p className="text-xl max-w-[270px] max-2xl:max-w-[500px]">
              If you're a Twitch Affiliate or Partner, you can use this bot to
              create 2-minute polls on your channel, as well as having the bot
              listen to channel point redemptions!
            </p>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}

export default Home;
