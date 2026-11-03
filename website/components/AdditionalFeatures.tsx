const AdditionalFeatures = () => {
  return (
    <>
      <h1 className="text-4xl text-center">Additional Features</h1>
      <div className="flex max-lg:flex-col gap-20 max-lg:gap-5 justify-center mt-5">
        <div className="additionalFeatureBlock">
          <h1 className="text-2xl font-bold">Redemptions Listener</h1>
          <p className="text-xl">
            Enable this and the bot will listen to your Twitch redemptions. Any
            redemption whose name starts with "Exchange" gets its cost added to
            the user's points in the bot's points system. For example, a
            50-point redemption adds 50 points to that user's balance.
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
