import { MagicWandIcon, MagnifyingGlassIcon } from "@radix-ui/react-icons"

import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator
} from "./ui/command"

export interface CommandModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const CommandModal = ({ open, onOpenChange }: CommandModalProps) => {
  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Documentation">
          <CommandItem>
            <MagicWandIcon className="mr-2 h-3 w-3" />
            <span>Ask AI...</span>
          </CommandItem>
          <CommandItem>
            <MagnifyingGlassIcon className="mr-2 h-3 w-3" />
            <span>Search the Documentation</span>
          </CommandItem>
        </CommandGroup>
        <CommandSeparator />
      </CommandList>
    </CommandDialog>
  )
}

export default CommandModal
