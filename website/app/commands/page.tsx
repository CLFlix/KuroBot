import Header from "@/components/Header";
import Footer from "@/components/Footer";
import CommandsClientView from "./CommandsClientView";

async function Commands() {
  return (
    <>
      <Header />
      <main className="m-10 mt-3 max-lg:mb-3">
        <section className="grid grid-cols-2 max-lg:grid-cols-1">
          <CommandsClientView />
        </section>
      </main>
      <Footer />
    </>
  );
}

export default Commands;
