import Chat from "@/components/chat"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent } from "@/components/ui/dialog"
import { MagicWandIcon } from "@radix-ui/react-icons"
import cssText from "data-text:~style.css"
import type { PlasmoCSConfig } from "plasmo"
import React, { useEffect } from "react"

import "~style.css"

export const config: PlasmoCSConfig = {
  matches: [
    "https://docs.convex.dev/*",
    "https://echo.labstack.com/docs/*",
    "https://tailwindcss.com/docs/*",
    "https://docs.airbyte.com/*"
  ]
}

export const getStyle = () => {
  const style = document.createElement("style")
  style.textContent = cssText
  return style
}

const PlasmoOverlay = () => {
  const [showDialog, setShowDialog] = React.useState(true)

  return (
    <>
      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent className="max-w-[52rem]">
          <Chat />
        </DialogContent>
      </Dialog>
      <Button
        size="lg"
        className="text-md fixed bottom-7 right-7 px-5 py-6 rounded-full"
        onClick={() => setShowDialog(true)}>
        Ask AI
        <MagicWandIcon className="ml-2 w-4 h-4" />
      </Button>
    </>
  )
}

export default PlasmoOverlay
