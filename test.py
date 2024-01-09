import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x300")


def button_click_event():
    dialog = ctk.CTkInputDialog(text="Type in a number:", title="Test")
    print("Number:", dialog.get_input())


def Error(entryType, errorType, number):
    # error = ctk.CTkInputDialog(
    #     self,
    #     title="Error",
    #     text=(str(entryType) + " must be " + str(errorType) + ": " + str(number)),
    # )

    error = ctk.CTkInputDialog(
        text=(str(entryType) + " must be " + str(errorType) + ": " + str(number)),
        title="Error",
    )

    flag = False

    if errorType.lower() == "greater than" and float(error.get_input()) > number:
        flag = True
    elif errorType.lower() == "less than" and float(error.get_input()) < number:
        flag = True
    elif errorType.lower() == "equal to" and float(error.get_input()) == number:
        flag = True
    elif errorType.lower() == "not equal to" and float(error.get_input()) != number:
        flag = True
    else:
        error.destroy()
        return

    return error.get_input() if flag else Error(entryType, errorType, number)


button = ctk.CTkButton(
    app, text="Open Dialog", command=Error("test", "greater than", 1)
)
button.pack(padx=20, pady=20)

app.mainloop()
