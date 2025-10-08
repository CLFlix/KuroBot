export interface Command {
  name: string;
  description: string;
  category: "useful" | "fun" | "redeem";
}
