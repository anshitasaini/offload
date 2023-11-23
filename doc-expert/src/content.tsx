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
  const [showDialog, setShowDialog] = React.useState(false)

  return (
    <>
      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent className="max-w-[52rem]">
          <Chat />
        </DialogContent>
      </Dialog>
      <Button
        size="lg"
        variant="outline"
        className="text-md fixed bottom-7 right-7 px-5 py-6 rounded-full"
        onClick={() => setShowDialog(true)}>
        Ask AI
        <img
          src="https://cf.appdrag.com/dashboard-openvm-clo-b2d42c/uploads/airbyte-1613152137-dKaX.png"
          alt="Airbyte Logo"
          className="w-7 h-7 ml-2"
        />
      </Button>
    </>
  )
}

export default PlasmoOverlay
