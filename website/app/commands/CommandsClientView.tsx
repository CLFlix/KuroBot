"use client";

import { useEffect, useState } from "react";
import CommandsTable from "@/components/commands/commandsTable";
import CommandsService from "@/services/CommandsService";
import { Command } from "@/types";

export default function Commands() {
  const [commands, setCommands] = useState<Command[]>([]);

  useEffect(() => {
    CommandsService.getAllCommands().then(setCommands);
  }, []);

  const grouped = commands.reduce<Record<string, Command[]>>((acc, cmd) => {
    const cat = cmd.category || "other";
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(cmd);
    return acc;
  }, {});

  return (
    <div className="space-y-8">
      {Object.entries(grouped).map(([category, list]) => (
        <section key={category}>
          <h2 className="text-xl font-bold mb-2 capitalize">
            {category} commands
          </h2>
          <CommandsTable commandsList={list} />
        </section>
      ))}
    </div>
  );
}
