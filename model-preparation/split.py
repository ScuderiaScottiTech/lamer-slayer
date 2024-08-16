import os, sys

def split_into_files(target_dir: str, prefix: str, messages: dict, delete_dir=False):
    if delete_dir:
        for file in os.listdir(target_dir):
            os.remove(f"{target_dir}/{file}")
        os.rmdir(target_dir)

    try:
        os.mkdir(target_dir)
    except FileExistsError:
        print("Warning: target dir exists you may be overwriting an existing dataset. Not creating.")
        # exit(1)
    
    for index, v in enumerate(messages.values()):
        f = open(f"{target_dir}/{prefix}-{index}.txt", "x")
        f.write(v["message"])
        f.close()
    
    print(f"Outputted {len(messages)} messages into {target_dir} for {prefix}")

# if __name__ == "__main__":
#     split_into_files(sys.argv[1])