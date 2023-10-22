import Chat from "@/components/chat"
import {
  Command,
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut
} from "@/components/ui/command"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from "@/components/ui/dialog"
import {
  CalendarIcon,
  EnvelopeClosedIcon,
  FaceIcon,
  GearIcon,
  MagicWandIcon,
  MagnifyingGlassIcon,
  PersonIcon,
  RocketIcon
} from "@radix-ui/react-icons"
import cssText from "data-text:~style.css"
import type { PlasmoCSConfig } from "plasmo"

import { CountButton } from "~features/count-button"

import "~style.css"

export const config: PlasmoCSConfig = {
  matches: ["https://docs.convex.dev/*", "https://news.ycombinator.com/*"]
}

export const getStyle = () => {
  const style = document.createElement("style")
  style.textContent = cssText
  return style
}

const PlasmoOverlay = () => {
  return (
    <Dialog open={true}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>AI Assistant</DialogTitle>
        </DialogHeader>
        <Chat />
      </DialogContent>
    </Dialog>
  )
  return (
    <CommandDialog open={true}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Documentation">
          <CommandItem>
            <MagicWandIcon className="mr-2 h-3 w-3" />
            <span>Ask Anshita AI...</span>
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

export default PlasmoOverlay
