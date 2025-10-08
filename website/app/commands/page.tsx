import Header from "@/components/Header";
import CommandsClientView from "./CommandsClientView";

async function Commands() {
  return (
    <>
      <Header />
      <main className="ml-auto">
        <h1 className="text-2xl text-center">Commands</h1>
        <CommandsClientView />
      </main>
    </>
  );
}

export default Commands;
