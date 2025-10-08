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

  return <CommandsTable commandsList={commands} />;
}
