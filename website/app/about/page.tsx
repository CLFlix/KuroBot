import Image from "next/image";

function About() {
  return (
    <>
      <main className="m-5 mb-10 mt-3 max-lg:mb-3 font-sans">
        <section className="grid grid-cols-2 max-lg:grid-cols-1">
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
              want it to do, I couldn't find one. Since I'm learning how to code
              in college, I got the idea to just make a bot of my own. I started
              out with a simple bot with commands like "?np" and "?rank",
              totaling about 70 lines of code. After adding more commands and a
              points system, I now have a bot with over 1,000 lines of code. I'm
              enjoying every step of the way, making my bot just a little better
              and more advanced each time.
            </p>
          </div>
          <div className="flex justify-center">
            <Image
              width={256}
              height={256}
              src={"/kurookami_logo.jpg"}
              alt="Kurookami logo"
              className="max-xl:hidden"
            ></Image>
          </div>
        </section>
        <section>
          <h1 className="text-3xl font-bold">Tech Stack</h1>
          <p>
            This bot was completely coded in Python. It uses the Twitch API for
            things like checking if a Twitch user exists{" "}
            <sub>("?gift" - bot points system)</sub> and adding VIP status to a
            user <sub>("vip")</sub>. The osu! API is also used to get the
            streamer's information to display the streamer's current rank,
            playtime and more. The website was made with React and Next.js +
            Tailwind CSS. It may look a little scuffed, since I had just started
            learning how to work with these frameworks in college when I built
            it. Tailwind CSS is responsible for the decent look of this website,
            since I SUCK at normal CSS.
          </p>
        </section>
        <section className="grid grid-cols-2 max-lg:grid-cols-1">
          <section>
            <h1 className="text-3xl font-bold mt-4">Contribute</h1>
            <h1 className="text-xl font-bold">Developers:</h1>
            <p>
              KuroBot is fully open-source, meaning anyone can contribute to the
              project! You can do so by forking the{" "}
              <a
                href="https://github.com/CLFlix/KuroBot"
                className="text-blue-400 hover:underline"
              >
                GitHub repo
              </a>{" "}
              and opening a pull request after making your desired changes.
            </p>
            <h1 className="text-xl font-bold">Anyone else:</h1>
            <p>
              Even if you don't know how to code, you can still contribute to
              the project! On the GitHub repo, there's a{" "}
              <a
                href="https://github.com/CLFlix/KuroBot/discussions"
                className="text-blue-400 hover:underline"
              >
                Discussions page
              </a>{" "}
              where you can submit suggestions for what YOU think the bot should
              be able to do. I'll be sure to check out every suggestion - just
              keep in mind that this is a side project and I have to put my main
              focus on college.
            </p>
          </section>
          <section className="text-center max-lg:hidden">
            <h1 className="text-3xl font-bold mt-4">Links</h1>
            <div className="flex flex-col gap-1 text-blue-400 text-xl">
              <span>
                <a
                  href="https://www.twitch.tv/kurookamitv"
                  className="hover:underline"
                >
                  Twitch
                </a>
              </span>
              <span>
                <a
                  href="https://www.youtube.com/@Doku_Kurookami"
                  className="hover:underline"
                >
                  YouTube
                </a>
              </span>
              <span>
                <a
                  href="https://www.tiktok.com/@_kurookami_osu"
                  className="hover:underline"
                >
                  TikTok
                </a>
              </span>
              <span>
                <a
                  href="https://discord.gg/4HAbQm2tdp"
                  className="hover:underline"
                >
                  Discord
                </a>
              </span>
              <span>
                <a
                  href="https://github.com/CLFlix/KuroBot"
                  className="hover:underline"
                >
                  GitHub Repo
                </a>
              </span>
            </div>
          </section>
        </section>
        <section className="text-center mt-4">
          <h1 className="text-3xl font-bold">Download</h1>
          <p className="font-bold">[REPLACE WITH LINK TO RELEASE]</p>
        </section>
      </main>
    </>
  );
}

export default About;
