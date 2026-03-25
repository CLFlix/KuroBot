import Image from "next/image";

function About() {
  return (
    <>
      <main className="m-5 mb-10 mt-3 max-xl:mb-3">
        <div className="grid grid-cols-2 max-xl:grid-cols-1">
          <div>
            <h1 className="text-3xl font-bold">Me!</h1>
            <p>
              Hi there! I'm Kurookami, also known as CLFlix - creator of this
              website and KuroBot. I'm a second-year college student studying
              Applied Computer Science, and a fanatic osu! player.
            </p>
            <h1 className="text-3xl font-bold mt-4">Why?</h1>
            <p>
              After searching for a chatbot that does everything I personally
              want it to do, I couldn't find one. I wanted it to have commands
              like <code>!np</code> and <code>!profile</code>, but I didn't want
              to have 4 different bots running on my channel. Since I'm learning
              how to code in college, I got the idea to just make a bot of my
              own. I started out with a simple bot with commands like{" "}
              <code>!np</code> and
              <code>!rank</code>, totaling about 70 lines of code. After adding
              more commands and a points system, I now have a bot with over
              1.000 lines of code. I'm enjoying every step of the way, making my
              bot just a little better and more advanced each time.
            </p>
            <h1 className="mt-4 text-3xl font-bold">Tech Stack</h1>
            <p>
              This bot was completely coded in Python. It uses the Twitch API
              for things like checking if a Twitch user exists{" "}
              <sub>("!gift" - bot points system)</sub> and adding VIP status to
              a user <sub>("vip")</sub>. The osu! API is also used to get the
              streamer's information to display the streamer's current rank,
              playtime and more. The website was made with React and Next.js +
              Tailwind CSS.
            </p>
            <h1 className="text-3xl font-bold mt-4">Contribute</h1>
            <h2 className="text-xl font-bold mt-1">Developers:</h2>
            <p>
              KuroBot is fully open-source, meaning anyone can contribute to the
              project! You can do so by forking the{" "}
              <a href="https://github.com/CLFlix/KuroBot" className="link">
                GitHub repo
              </a>{" "}
              and opening a pull request after making your desired changes.
            </p>
            <h2 className="text-xl font-bold mt-1">Anyone else:</h2>
            <p>
              Even if you don't know how to code, you can still contribute to
              the project! On the GitHub repo, there's a{" "}
              <a
                href="https://github.com/CLFlix/KuroBot/discussions/categories/suggestions"
                className="link"
              >
                Discussions page
              </a>{" "}
              where you can submit suggestions for what YOU think the bot should
              be able to do. I'll be sure to check out every suggestion - just
              keep in mind that this is a side project and I have to put my main
              focus on college. If you find errors or bugs, you can report these
              in the{" "}
              <a
                href="https://github.com/CLFlix/KuroBot/issues"
                className="link"
              >
                Issues page
              </a>
              , giving me a heads up.
            </p>
          </div>
          <div className="flex justify-center">
            <Image
              width={480}
              height={600}
              src={"static/logo.png"}
              alt="KuroBot Logo"
              className="max-xl:hidden rounded-2xl"
            ></Image>
          </div>
        </div>
        <div className="grid grid-cols-2 max-lg:grid-cols-1">
          <div className="text-center max-lg:hidden">
            <h1 className="text-3xl font-bold mt-4">Links</h1>
            <div className="flex flex-col gap-1 text-blue-400 text-xl">
              <span>
                <a
                  href="https://www.twitch.tv/kurookamitv"
                  className="big-link"
                >
                  Twitch
                </a>
              </span>
              <span>
                <a
                  href="https://www.youtube.com/@Doku_Kurookami"
                  className="big-link"
                >
                  YouTube
                </a>
              </span>
              <span>
                <a
                  href="https://www.tiktok.com/@_kurookami_osu"
                  className="big-link"
                >
                  TikTok
                </a>
              </span>
              <span>
                <a href="https://discord.gg/4HAbQm2tdp" className="big-link">
                  Discord
                </a>
              </span>
              <span>
                <a
                  href="https://github.com/CLFlix/KuroBot"
                  className="big-link"
                >
                  GitHub Repo
                </a>
              </span>
            </div>
          </div>
          <div className="text-center mt-4 pb-2">
            <h1 className="text-3xl font-bold">Download</h1>
            <a
              href="https://github.com/CLFlix/KuroBot/releases/tag/v2.1.0"
              className="link font-bold text-xl"
              target="_blank"
            >
              KuroBot v2.1.0
            </a>
          </div>
        </div>
      </main>
    </>
  );
}

export default About;
