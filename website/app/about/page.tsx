import Header from "@/components/Header";
import Image from "next/image";

function About() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex flex-col items-center justify-center flex-1">
        <Image
          src="/wip.png"
          width={200}
          height={200}
          alt="Attention board"
        />
        <section className="text-center mt-4">
          <h1 className="text-3xl">About</h1>
          <p>Work in progress...</p>
        </section>
      </main>
    </div>
  );
}

export default About;
