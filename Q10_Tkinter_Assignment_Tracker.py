"""Q10: Tkinter assignment tracker with JSON persistence and CSV export."""
import csv
import json
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

DATA_FILE = Path("assignments.json")
FIELDS = ["enrollment", "name", "assignment", "status", "marks", "remarks"]


class AssignmentTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Assignment Tracker")
        self.root.geometry("900x560")
        self.records = self.load_records()
        self.build_ui()
        self.refresh()

    def load_records(self):
        if not DATA_FILE.exists():
            return []
        try:
            with DATA_FILE.open(encoding="utf-8") as handle:
                data = json.load(handle)
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            messagebox.showwarning("Data warning", "Could not read assignments.json. Starting with an empty list.")
            return []

    def save_records(self):
        with DATA_FILE.open("w", encoding="utf-8") as handle:
            json.dump(self.records, handle, indent=2, ensure_ascii=False)

    def build_ui(self):
        form = ttk.LabelFrame(self.root, text="Submission details", padding=10)
        form.pack(fill="x", padx=12, pady=10)

        self.entries = {}
        labels = [("Enrollment", "enrollment"), ("Student name", "name"),
                  ("Assignment", "assignment"), ("Marks", "marks"), ("Remarks", "remarks")]
        for index, (label, key) in enumerate(labels):
            ttk.Label(form, text=label).grid(row=0, column=index, sticky="w", padx=4)
            entry = ttk.Entry(form, width=18)
            entry.grid(row=1, column=index, padx=4, pady=4, sticky="ew")
            self.entries[key] = entry

        ttk.Label(form, text="Status").grid(row=0, column=5, sticky="w", padx=4)
        self.status = tk.StringVar(value="Pending")
        ttk.Combobox(form, textvariable=self.status, values=["Pending", "Completed"],
                     state="readonly", width=14).grid(row=1, column=5, padx=4)

        buttons = ttk.Frame(self.root)
        buttons.pack(fill="x", padx=12)
        ttk.Button(buttons, text="Add / Update", command=self.add_or_update).pack(side="left", padx=4)
        ttk.Button(buttons, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=4)
        ttk.Button(buttons, text="Export CSV", command=self.export_csv).pack(side="left", padx=4)
        ttk.Label(buttons, text="Filter:").pack(side="left", padx=(20, 4))
        self.filter_status = tk.StringVar(value="All")
        filter_box = ttk.Combobox(buttons, textvariable=self.filter_status,
                                  values=["All", "Pending", "Completed"], state="readonly", width=12)
        filter_box.pack(side="left")
        filter_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh())

        columns = ("enrollment", "name", "assignment", "status", "marks", "remarks")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings", height=16)
        for column in columns:
            self.table.heading(column, text=column.title())
            self.table.column(column, width=130 if column != "remarks" else 220)
        self.table.pack(fill="both", expand=True, padx=12, pady=10)
        self.table.bind("<<TreeviewSelect>>", self.populate_form)

    def add_or_update(self):
        data = {key: entry.get().strip() for key, entry in self.entries.items()}
        if not data["enrollment"] or not data["name"] or not data["assignment"]:
            messagebox.showerror("Validation", "Enrollment, student name and assignment are required.")
            return
        if data["marks"]:
            try:
                marks = float(data["marks"])
                if marks < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Validation", "Marks must be a non-negative number.")
                return
        data["status"] = self.status.get()
        selected = self.table.selection()
        if selected:
            index = int(self.table.item(selected[0], "tags")[0])
            self.records[index] = data
        else:
            self.records.append(data)
        self.save_records()
        self.refresh()
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def populate_form(self, _event=None):
        selected = self.table.selection()
        if not selected:
            return
        index = int(self.table.item(selected[0], "tags")[0])
        record = self.records[index]
        for key, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, record.get(key, ""))
        self.status.set(record.get("status", "Pending"))

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Select record", "Choose a row to delete.")
            return
        index = int(self.table.item(selected[0], "tags")[0])
        del self.records[index]
        self.save_records()
        self.refresh()

    def refresh(self):
        for item in self.table.get_children():
            self.table.delete(item)
        chosen = self.filter_status.get()
        for index, record in enumerate(self.records):
            if chosen != "All" and record.get("status") != chosen:
                continue
            self.table.insert("", "end", values=[record.get(key, "") for key in FIELDS],
                              tags=(str(index),))

    def export_csv(self):
        path = Path("assignment_report.csv")
        try:
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(self.records)
            messagebox.showinfo("Export complete", f"Report saved to {path.resolve()}")
        except OSError as exc:
            messagebox.showerror("Export failed", str(exc))


if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentTracker(root)
    root.mainloop()
