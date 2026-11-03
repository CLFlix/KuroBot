const AdditionalFeatures = () => {
  return (
    <>
      <h1 className="text-4xl text-center">Additional Features</h1>
      <div className="flex max-lg:flex-col gap-20 max-lg:gap-5 justify-center mt-5">
        <div className="additionalFeatureBlock">
          <h1 className="text-2xl font-bold">Redemptions Listener</h1>
          <p className="text-xl">
            If you enable this, the bot will listen to all the redemptions made
            on your Twitch channel! With how things are right now, the bot will
            only recognize redemptions whose name starts with "Exchange". The
            bot will then add the cost of the Twitch redemption to its own
            points system. I'll give a quick example: If the Twitch redemption
            costed 500 points, the bot will then add 500 points to the amount of
            points this user has in the bot's points system.
          </p>
        </div>
        <div className="additionalFeatureBlock">
          <h1 className="text-2xl font-bold">Automatic Title Updater</h1>
          <p className="text-xl">
            By enabling this, you can let the bot check whether your osu! rank
            has changed in comparison to what's stated in the title. If your
            rank did change, the bot will update your Twitch stream's title with
            your current osu! rank, keeping your audience up-to-date!
          </p>
        </div>
      </div>
    </>
  );
};

export default AdditionalFeatures;
