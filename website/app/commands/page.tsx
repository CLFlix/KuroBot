import Header from "@/components/Header";
import Footer from "@/components/Footer";
import CommandsClientView from "./CommandsClientView";

async function Commands() {
  return (
    <>
      <Header />
      <main className="mt-2 max-lg:mb-13">
        <section className="grid grid-cols-2 max-lg:grid-cols-1">
          <CommandsClientView />
        </section>
      </main>
      <Footer />
    </>
  );
}

export default Commands;
