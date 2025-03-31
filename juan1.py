"""
The Juan One chat bot. A simple bot that will be used as the stepping stone into ML and AI.
Currently, there is no actual ML, but that is planned to change after the first release.
"""
import json
import re
import os
import error_responses

JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "responses.json")
APP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "known_applications.json")

class Juan:
    """
    The Juan class is the main class for the Juan One chat bot.
    It is the entry point for the bot and contains the main logic for the bot.
    """
    def __init__(self,verbose=False):
        self.json_data = self.get_json(JSON_PATH)
        self.verbose = verbose
        self.known_applications = self.get_json(APP_PATH)

    def get_json(self,file_path):
        """
        Load JSON data.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def write_json(self,data,file_path):
        """
        Write JSON data to a file.
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def define_applications(self):
        """
        Define applications that the bot can open.
        """
        print("Juan: It looks like you are trying to open an application, but I don't know what"+
        " applications you have installed. Would you like to define them now?\n[y/N]")
        user_input = input("You: ")
        data = self.get_json(APP_PATH)
        if self.verbose:
            print(f"DEBUG: data: {data}")
        if data is not dict:
            data = {}
            if self.verbose:
                print("DEBUG: data is not a dict, defining new empty dict")
        if user_input.lower() in ["yes", "y"]:
            print("Juan: Great! Please provide the name of the application and the path to the executable."+
                  "Note that order matters! The first input will be the name of the application, "+
                  "and the second will be the path to the executable.\n"+
                  "EG: Chrome, C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"+
                  "\n\nIf you would like to stop defining applications, type 'exit', 'quit', or 'q' at any time.\n")
            define_applications = True
            while define_applications:
                path_info = input("You: ")
                if path_info.lower() in ["exit", "quit", "q"]:
                    print("Juan: Done defining applications.")
                    print("Juan: Would you like to save the applications you defined?\n[Y/n]")
                    if input("You: ").lower() in ["no", "n"]:
                        break
                    else:
                        print("Juan: Saving applications...")
                        self.write_json(data, APP_PATH)
                        print("Juan: Applications saved.")
                    define_applications = False
                    break

                splitpath = re.split(r'\s+|[.,;:!?-]\s*', path_info.lower())
                if self.verbose:
                    print(f"DEBUG: splitpath: {splitpath}")
                if len(splitpath) != 2:
                    print("Juan: It looks like you didn't provide the correct number of inputs. Please try again.")
                    continue
                else:
                    app_name = splitpath[0]
                    app_path = splitpath[1]
                    if self.verbose:
                        print(f"DEBUG: app_name: {app_name}\napp_path: {app_path}")
                    if os.path.exists(app_path):
                        if self.verbose:
                            print(f"DEBUG: Found application: {app_name}\nPath: {app_path}")
                        data[app_name] = app_path


    def handle_action(self,idx,user_input):
        """
        Handle an action based on the action type.
        """
        if self.known_applications is None:
            self.define_applications()
            self.known_applications = self.get_json(APP_PATH)
        try:
            if self.json_data[idx]["action_type"] == "open":
                found_app = False
                for app, path in self.known_applications.items():
                    if app in user_input.lower():
                        try:
                            found_app = True
                            if self.verbose:
                                print(f"DEBUG: Found application: {app}\nPath: {path}")
                            os.system(path)
                            return ["success_response", self.json_data[idx]["response"].format(app)]
                        except FileExistsError as e:
                            if self.verbose:
                                print(f"DEBUG: Error opening application: {e}")
                            return ["failure_response", error_responses.failure_response()]
                        except Exception as e:
                            if self.verbose:
                                print(f"DEBUG: Unexpected error: {e}")
                            return ["failure_response", error_responses.failure_response()]
                if not found_app:
                    return ["failure_response", error_responses.no_app_found()]
            elif self.json_data[idx]["action_type"] == "list_known_apps":
                if self.known_applications is None:
                    return ["failure_response", error_responses.no_defined_apps()]
                if self.verbose:
                    print(f"DEBUG: Known applications: {self.known_applications}")
                apps = ""
                for app in self.known_applications:
                    apps += app + ", "
                    if self.verbose:
                        print(f"DEBUG: app: {app}")
                apps = apps[:-2]  # Remove the last comma and space
                return ["success_response", self.json_data[idx]["response"].format(apps)]
        except KeyError as e:
            if self.verbose:
                print(f"DEBUG: KeyError: {e}")
            return ["failure_response", error_responses.failure_response()]
        except AttributeError as e:
            if self.verbose:
                print(f"DEBUG: AttributeError: {e}")
            return ["failure_response", error_responses.failure_response()]
        except Exception as e:
            if self.verbose:
                print(f"DEBUG: Unexpected error: {e}")
            return ["failure_response", error_responses.failure_response()]

    def get_response(self, user_input):
        """
        Get a response from the bot based on the user input.
        """
        if self.json_data is None:  # Load JSON data if not already loaded
            self.get_json(JSON_PATH)

        if self.json_data is None: # If JSON data could not be loaded, return an error message
            return ["data_error", error_responses.data_failure()]

        if user_input == "":
            return ["no_input",error_responses.no_input()]

        split_input = re.split(r'\s+|[.,;:!?-]\s*', user_input.lower())
        scores = []

        if self.verbose:
            print(f"DEBUG: split_input: {split_input}")
        # if self.verbose: # Uncommenting will print the entire json data, use with caution
        #     print(f"DEBUG: json_data: {self.json_data}")
        for response in self.json_data:
            # if self.verbose: # Uncommenting will print the entire response for every response
            #     print(f"DEBUG: response: {response}")
            response_score = 0
            required_score = 0
            required_words = response["required_words"]
            if self.verbose:
                print(f"DEBUG: required_words: {required_words}")

            if required_words:
                for word in split_input:
                    for requirement in enumerate(required_words):
                        if self.verbose:
                            print(f"DEBUG: requirement: {requirement}")
                        idx = requirement[0]
                        if word in required_words[idx]:
                            if self.verbose:
                                print(f"DEBUG: Word found: {word}\nRequired word: {required_words[idx]}")
                            required_score +=1
                            if self.verbose:
                                print(f"DEBUG: Required word found: {word}\nScore: {required_score}")

            if required_score == len(required_words):
                for word in split_input:
                    if word in response["user_input"]:
                        response_score += 1
                        if self.verbose:
                            print(f"DEBUG: Word found: {word}\nResponse Score: {response_score}")
            scores.append(response_score)
            if self.verbose:
                print(f"DEBUG: scores: {scores}")

        if not scores:
            return ["failure_response", error_responses.failure_response()]

        best_response = max(scores)
        response_index = scores.index(best_response)

        if self.json_data[response_index]["type"] == "action":
            return self.handle_action(response_index,user_input)

        if best_response != 0:
            return [self.json_data[response_index]["type"],
                    self.json_data[response_index]["response"]]

        else:
            return ["failure_response",error_responses.failure_response()]

def main():
    """
    This is the CLI connection between the user and Juan.
    """
    verbose = False
    juan = Juan(verbose=verbose)

    greeter = "Juan 1.1 \n"
    main_instance = True

    auto_closing_types = ['goodbye','data_error']

    print(greeter)
    while main_instance:
        main_input = input("You: ")

        # juan_response will be ["type","bot response"]
        juan_response = juan.get_response(main_input)
        if verbose:
            print(f"DEBUG: {juan_response}")

        print("Juan:", juan_response[1])
        if juan_response[0] in auto_closing_types:
            main_instance = False
            if verbose:
                print(f"DEBUG: Auto closing type: {juan_response[0]}")
                print("DEBUG: Closing")
            input()

if __name__ == "__main__":
    main()
