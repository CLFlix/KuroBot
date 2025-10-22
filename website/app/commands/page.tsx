import CommandsClientView from "./CommandsClientView";

async function Commands() {
  return (
    <>
      <main className="m-10 mt-3 mb-15">
        <h1 className="text-4xl text-center">Commands</h1>
        <section className="grid grid-cols-2 max-lg:grid-cols-1">
          <CommandsClientView />
        </section>
        <h1 className="text-4xl text-center">Additional Features</h1>
        <section className="flex max-2xl:grid max-2xl:grid-cols-2 gap-10 justify-center mt-5">
          <div className="bg-gradient-to-tr from-purple-700 to-purple-900 rounded-lg p-1 text-center">
            <h1 className="text-2xl font-bold">Redemptions Listener</h1>
            <p className="text-xl max-w-[410px] max-2xl:max-w-[400px]">
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
          <div className="bg-gradient-to-tl from-purple-700 to-purple-900 rounded-lg p-1 text-center">
            <h1 className="text-2xl font-bold">Automatic Title Updater</h1>
            <p className="text-xl max-w-[410px] max-2xl:max-w-[400px]">
              By enabling this, you can let the bot check whether your osu! rank
              has changed in comparison to what's stated in the title. If your
              rank did change, the bot will update your Twitch stream's title
              with your current osu! rank, keeping your audience up-to-date!
              This will only work if you have your rank in between brackets:
              "[]". If you have multiple things between brackets in your title,
              keep your rank in the first pair of brackets.
            </p>
          </div>
        </section>
      </main>
    </>
  );
}

export default Commands;
