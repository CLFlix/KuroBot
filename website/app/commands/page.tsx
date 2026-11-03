import AdditionalFeatures from "@/components/AdditionalFeatures";
import CommandsClientView from "@/components/commands/CommandsClientView";

async function Commands() {
  return (
    <>
      <main className="m-10 mt-3 mb-15">
        <h1 className="text-4xl text-center">Commands</h1>
        <div className="grid grid-cols-2 max-lg:grid-cols-1">
          <CommandsClientView />
        </div>
        <AdditionalFeatures />
      </main>
    </>
  );
}

export default Commands;
