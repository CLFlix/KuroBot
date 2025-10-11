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

  return Object.entries(grouped).map(([category, list]) => {
    const displayCategory =
      category.toLowerCase() === "osu" ? "osu!" : category;

    return (
      <section key={category}>
        <h2
          className={
            displayCategory === "osu!"
              ? "text-center text-2xl font-bold mb-2"
              : "text-center text-2xl font-bold mb-2 capitalize"
          }
        >
          {displayCategory} commands
        </h2>
        <CommandsTable commandsList={list} />
      </section>
    );
  });
}
