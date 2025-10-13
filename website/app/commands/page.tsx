import CommandsClientView from "./CommandsClientView";

async function Commands() {
  return (
    <>
      <main className="m-10 mt-3 max-lg:mb-3">
        <section className="grid grid-cols-2 max-lg:grid-cols-1">
          <CommandsClientView />
        </section>
      </main>
    </>
  );
}

export default Commands;
