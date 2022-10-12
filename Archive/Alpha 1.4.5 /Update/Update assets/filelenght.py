# /Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_1.txt
# /Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_2.txt
# /Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_3.txt
# /Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_4.txt
# /Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_5.txt

paths = [
    "/Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_1.txt",
    "/Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_2.txt",
    "/Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_3.txt",
    "/Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_4.txt",
    "/Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_5.txt",

    "/Users/cmauro/Programs/Xenakis/batch_1.txt",
    "/Users/cmauro/Programs/Xenakis/batch_2.txt",
    "/Users/cmauro/Programs/Xenakis/batch_3.txt",
    "/Users/cmauro/Programs/Xenakis/batch_4.txt"
]



# path = "/Users/cmauro/Programs/Xenakis/Assets/Richard/txt chunks/chunk_4.txt"
counter = 1
for path in paths:
    with open (path, "r") as f:
        data = f.read()
    speratated = data.split("]]")
    print(len(speratated))




# Try with 10k maximun events per string file