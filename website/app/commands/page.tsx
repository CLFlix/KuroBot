import Header from "@/components/Header";
import CommandsClientView from "./CommandsClientView";

async function Commands() {
  return (
    <>
      <Header />
      <main className="mt-3">
        <section className="grid grid-cols-2">
          <CommandsClientView />
        </section>
      </main>
    </>
  );
}

export default Commands;
