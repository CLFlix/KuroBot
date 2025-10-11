import Header from "@/components/Header";
import Footer from "@/components/Footer";
import CommandsClientView from "./CommandsClientView";

async function Commands() {
  return (
    <>
      <Header />
      <main className="mt-2">
        <section className="grid grid-cols-2">
          <CommandsClientView />
        </section>
      </main>
      <Footer />
    </>
  );
}

export default Commands;
