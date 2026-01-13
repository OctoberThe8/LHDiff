import tkinter as tk
from tkinter import ttk
from typing import List, Dict


# Pastel colors matching your sketch
COLOR_DELETED = "#f8d7da"  # light red
COLOR_SPLIT   = "#d1e7dd"  # light green
COLOR_SAME    = "#dbeafe"  # light blue
COLOR_ADDED   = "#fef9c3"  # light yellow
COLOR_DEFAULT = "white"

# compute status of the lines on the left (deleted or split or same) for each line so we can color them.
# compute status of the lines on the right (added or split or same) for each line so we can color them.
def classifyLines(
    leftLines: List[str],
    rightLines: List[str],
    mapping: Dict[int, List[int]],
):
    
    numberLeft = len(leftLines)
    numberRight = len(rightLines)

    leftStatus = ["deleted"] * numberLeft
    rightStatus = ["added"] * numberRight

    #build reverse mapping: which left lines point to each right line
    rightToLeft: Dict[int, List[int]] = {}
    for lineIndex, r_list in mapping.items():
        if not r_list:
            continue
        if len(r_list) == 1:
            leftStatus[lineIndex] = "same"
        else:
            leftStatus[lineIndex] = "split"

        for r_idx in r_list:
            rightToLeft.setdefault(r_idx, []).append(lineIndex)

    #classify right side
    for r_idx in range(numberRight):
        if r_idx not in rightToLeft:
            rightStatus[r_idx] = "added"
            continue

        ls = rightToLeft[r_idx]
        #if any of its left lines is a split mapping, mark as split
        split_here = any(
            len(mapping[l]) > 1
            for l in ls
            if l in mapping
        )
        if split_here:
            rightStatus[r_idx] = "split"
        else:
            rightStatus[r_idx] = "same"
    return leftStatus, rightStatus
#define the colors to each satus
def statusToColor(status: str) -> str:
    if status == "deleted":
        return COLOR_DELETED
    if status == "split":
        return COLOR_SPLIT
    if status == "same":
        return COLOR_SAME
    if status == "added":
        return COLOR_ADDED
    return COLOR_DEFAULT


def runLineTracker(
    leftLines: List[str],
    rightLines: List[str],
    mapping: Dict[int, List[int]],
) -> None:
    root = tk.Tk()
    root.title("Line Tracker")
    root.configure(bg="white")
    root.minsize(950, 550)

    #overall grid
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # tOP: TITLE  
    top = ttk.Frame(root, padding=10)
    top.grid(row=0, column=0, sticky="ew")
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=0)

    titleLabel = tk.Label(
        top,
        text="Line Tracker",
        font=("Segoe UI", 18, "bold"),
        bg="white",
    )
    titleLabel.grid(row=0, column=0, sticky="w")

    subtitle = tk.Label(
        top,
        text="Click a line on the left only to see its corresponding line(s) summary on the right.",
        font=("Segoe UI", 9),
        fg="#555555",
        bg="white",
    )
    subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))

    #legend on the right (top)
    legendFrame = tk.Frame(top, bg="white")
    legendFrame.grid(row=0, column=1, rowspan=2, sticky="e", padx=(20, 0))

    def legendItem(color, text, row):
        swatch = tk.Label(
            legendFrame,
            bg=color,
            width=2,
            height=1,
            relief="solid",
            bd=1,
        )
        swatch.grid(row=row, column=0, padx=(0, 5), pady=1, sticky="w")
        lbl = tk.Label(
            legendFrame,
            text=text,
            font=("Segoe UI", 9),
            bg="white",
        )
        lbl.grid(row=row, column=1, sticky="w")

    legendItem(COLOR_DELETED, "for lines that are deleted", 0)
    legendItem(COLOR_SPLIT,   "for lines that got split",   1)
    legendItem(COLOR_SAME,    "for lines that are same",    2)
    legendItem(COLOR_ADDED,   "for lines that are added",   3)

    #MIDDLE: LEFT / RIGHT COLUMNS
    middle = tk.Frame(root, bg="white")
    middle.grid(row=1, column=0, sticky="nsew", padx=10)
    middle.rowconfigure(1, weight=1)
    middle.columnconfigure(0, weight=1)
    middle.columnconfigure(1, weight=1)

    #compute statuses for coloring
    leftStatus, rightStatus = classifyLines(leftLines, rightLines, mapping)

    #left panel
    leftPanel = tk.Frame(middle, bg="white", bd=1, relief="solid")
    leftPanel.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
    leftPanel.rowconfigure(1, weight=1)
    leftPanel.columnconfigure(0, weight=1)

    leftHeader = tk.Label(
        leftPanel,
        text="Left",
        font=("Segoe UI", 12, "bold"),
        bg="white",
    )
    leftHeader.grid(row=0, column=0, sticky="w", padx=8, pady=4)

    leftScroll = tk.Scrollbar(leftPanel, orient="vertical")
    leftList = tk.Listbox(
        leftPanel,
        yscrollcommand=leftScroll.set,
        font=("Consolas", 10),
        bd=0,
        highlightthickness=0,
    )
    leftScroll.config(command=leftList.yview)
    leftList.grid(row=1, column=0, sticky="nsew", padx=(4, 0), pady=(0, 4))
    leftScroll.grid(row=1, column=1, sticky="ns", pady=(0, 4))

    #right panel
    rightPanel = tk.Frame(middle, bg="white", bd=1, relief="solid")
    rightPanel.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
    rightPanel.rowconfigure(1, weight=1)
    rightPanel.columnconfigure(0, weight=1)

    rightHeader = tk.Label(
        rightPanel,
        text="Right",
        font=("Segoe UI", 12, "bold"),
        bg="white",
    )
    rightHeader.grid(row=0, column=0, sticky="w", padx=8, pady=4)

    rightScroll = tk.Scrollbar(rightPanel, orient="vertical")
    rightList = tk.Listbox(
        rightPanel,
        yscrollcommand=rightScroll.set,
        font=("Consolas", 10),
        bd=0,
        highlightthickness=0,
        selectmode="extended",
    )
    rightScroll.config(command=rightList.yview)
    rightList.grid(row=1, column=0, sticky="nsew", padx=(4, 0), pady=(0, 4))
    rightScroll.grid(row=1, column=1, sticky="ns", pady=(0, 4))

    #populate Left with colors
    for i, line in enumerate(leftLines):
        display = f"{i+1:>3}  {line}"
        idx = leftList.size()
        leftList.insert(tk.END, display)
        leftList.itemconfig(idx, {"bg": statusToColor(leftStatus[i])})

    #populate Right with colors
    for j, line in enumerate(rightLines):
        display = f"{j+1:>3}  {line}"
        idx = rightList.size()
        rightList.insert(tk.END, display)
        rightList.itemconfig(idx, {"bg": statusToColor(rightStatus[j])})

    #BOTTOM: TEXT SUMMARY 
    bottom = tk.Frame(root, bg="white")
    bottom.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
    bottom.columnconfigure(0, weight=1)

    summaryLabel = tk.Label(
        bottom,
        text="Summary",
        font=("Segoe UI", 10, "bold"),
        bg="white",
    )
    summaryLabel.grid(row=0, column=0, sticky="w")

    summaryText = tk.Text(
        bottom,
        height=4,
        font=("Segoe UI", 9),
        wrap="word",
        bd=1,
        relief="solid",
    )
    summaryText.grid(row=1, column=0, sticky="ew", pady=(2, 0))
    summaryText.insert("1.0", "Click on a line on the Left to see its formula-style mapping here.")
    summaryText.config(state="disabled")

    #helper to write into summary box
    def setSummary(text: str):
        summaryText.config(state="normal")
        summaryText.delete("1.0", tk.END)
        summaryText.insert("1.0", text)
        summaryText.config(state="disabled")

    #CLICK HANDLER 
    def onLeftSelect(event=None):
        #clear selection on right
        rightList.selection_clear(0, tk.END)

        sel = leftList.curselection()
        if not sel:
            return

        lineIndex = sel[0]  #0-based
        lineNumber = lineIndex + 1
        mapped = mapping.get(lineIndex, [])

        if not mapped:
            #deleted
            msg = f"Left line {lineNumber} → deleted"
        else:
            mappedLines = [r + 1 for r in mapped]  #1-based for user
            if len(mapped) == 1:
                msg = f"Left line {lineNumber} → Right line {mappedLines[0]}"
            else:
                msg = f"Left line {lineNumber} → Right lines {mappedLines}  (split)"

            #highlight mapped right lines
            for r_idx in mapped:
                if 0 <= r_idx < rightList.size():
                    rightList.selection_set(r_idx)
                    rightList.see(r_idx)
        #also mention added right lines at the end
        added = [
            r + 1
            for r, status in enumerate(rightStatus)
            if status == "added"
        ]
        if added:
            msg += f"\nRight lines {added} → added"

        setSummary(msg)
    leftList.bind("<<ListboxSelect>>", onLeftSelect)
    root.mainloop()

#  DEMO to test the code 
if __name__ == "__main__":
    left_demo = [
        "x = a + b;",
        "return x;",
        "total = a + b + c;",
        "why",
    ]
    right_demo = [
        "x = a",
        "+ b;",
        "return x;",
        "total = a",
        "+ b",
        "+ c;",
        "w += 0;",
    ]
    mapping_demo = {
        0: [0, 1],      
        1: [2],         
        2: [3, 4, 5],   
    }
#call the function to do the gui, mapping_demo that will come from Parsia's code when we will use the code for the final output for all the tests
    runLineTracker(left_demo, right_demo, mapping_demo)