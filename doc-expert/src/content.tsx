import Chat from "@/components/chat"
import CommandModal from "@/components/command-modal"
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
import React from "react"

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
  const [showDialog, setShowDialog] = React.useState(false)

  React.useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.metaKey && event.key === "j") {
        setShowDialog((showDialog) => !showDialog)
      }
    }
    window.addEventListener("keydown", handleKeyDown)

    return () => {
      window.removeEventListener("keydown", handleKeyDown)
    }
  }, [])

  return <CommandModal open={showDialog} onOpenChange={setShowDialog} />
  return (
    <Dialog open={showDialog} onOpenChange={setShowDialog}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>AI Assistant</DialogTitle>
        </DialogHeader>
        <Chat />
      </DialogContent>
    </Dialog>
  )
}

export default PlasmoOverlay
