import subprocess
import re

def run_powermetrics_and_save(samples=1):
    try:
        # Run the powermetrics command and save its output to a file
        output = subprocess.check_output([
            "sudo", "powermetrics", "--samplers", "gpu_power", f"-n{samples}"
        ], stderr=subprocess.DEVNULL).decode()

        # Save the output to a file for debugging
        with open("powermetrics_output.txt", "w") as f:
            f.write(output)

        # Display the saved content using `cat` to inspect
        print("Displaying powermetrics output:")
        subprocess.run(["cat", "powermetrics_output.txt"])

        return output

    except subprocess.CalledProcessError as e:
        return f"Error running powermetrics: {str(e)}"

def get_gpu_stats(samples=1):
    try:
        # Run powermetrics and save the output
        output = run_powermetrics_and_save(samples)

        # If output is empty, it may indicate unsupported GPU stats
        if not output:
            return [{"Error": "GPU stats are unsupported on this system."}]

        # Parse the output for relevant GPU stats
        samples_data = output.split("*** Sampled system activity")
        parsed_samples = []

        for sample in samples_data:
            if "**** GPU usage ****" not in sample:
                continue

            gpu_data = {}

            freq_match = re.search(r"GPU HW active frequency:\s+(\d+)\s+MHz", sample)
            if freq_match:
                gpu_data["Active Frequency"] = f"{freq_match.group(1)} MHz"

            residency_match = re.search(r"GPU HW active residency:\s+([\d\.]+%)", sample)
            if residency_match:
                gpu_data["HW Active Residency"] = residency_match.group(1)

            idle_match = re.search(r"GPU idle residency:\s+([\d\.]+%)", sample)
            if idle_match:
                gpu_data["Idle Residency"] = idle_match.group(1)

            power_match = re.search(r"GPU Power:\s+(\d+)\s+mW", sample)
            if power_match:
                gpu_data["GPU Power"] = f"{power_match.group(1)} mW"

            parsed_samples.append(gpu_data)

        if not parsed_samples:
            return [{"Error": "No GPU stats found."}]

        return parsed_samples

    except subprocess.CalledProcessError as e:
        # Specific error handling for when powermetrics fails
        return [{"Error": "The powermetrics tool is not supported or available."}]
    except Exception as e:
        return [{"Error": f"An unexpected error occurred: {str(e)}"}]

# Example usage
if __name__ == "__main__":
    print(get_gpu_stats())
