import CommandsClientView from "./CommandsClientView";

async function Commands() {
  return (
    <>
      <main className="m-10 mt-3 mb-15">
        <h1 className="text-4xl text-center">Commands</h1>
        <div className="grid grid-cols-2 max-lg:grid-cols-1">
          <CommandsClientView />
        </div>
        <h1 className="text-4xl text-center">Additional Features</h1>
        <div className="flex max-2xl:flex-col gap-20 max-2xl:gap-5 justify-center mt-5">
          <div className="text-block-gradient rounded-lg p-2 text-center max-w-[23%] border border-gray-600 max-2xl:max-w-full">
            <h1 className="text-2xl font-bold">Redemptions Listener</h1>
            <p className="text-xl">
              If you enable this, the bot will listen to all the redemptions
              made on your Twitch channel! With how things are right now, the
              bot will only recognize redemptions whose name starts with
              "Exchange". The bot will then add the cost of the Twitch
              redemption to its own points system. I'll give a quick example: If
              the Twitch redemption costed 500 points, the bot will then add 500
              points to the amount of points this user has in the bot's points
              system.
            </p>
          </div>
          <div className="text-block-gradient rounded-lg p-2 text-center max-w-[23%] border border-gray-600 max-2xl:max-w-full">
            <h1 className="text-2xl font-bold">Automatic Title Updater</h1>
            <p className="text-xl">
              By enabling this, you can let the bot check whether your osu! rank
              has changed in comparison to what's stated in the title. If your
              rank did change, the bot will update your Twitch stream's title
              with your current osu! rank, keeping your audience up-to-date!
              This will only work if you have your rank in between brackets:
              "[]". If you have multiple things between brackets in your title,
              keep your rank in the first pair of brackets.
            </p>
          </div>
        </div>
      </main>
    </>
  );
}

export default Commands;
