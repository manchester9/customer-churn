- - KF V2
    -  Ways to create components, status:
        - We are moving away from func_to_container_op in KFPv1, we suggest to use create_component_from_func in KFPv1.
        - For KFPv2, we are moving away from both approaches above. We recommend using @component decorator in KFPv2.
    - default machine type is e2-standard-4, we can make it e2-highmem-2 with set_cpu_limit('1') and set_memory_limit('3G').\

    - use run name to get run id


    - Containerized python components extend lightweight componenets by relaxing the constraint that lightweight python componenets be hermetic (fully self-contained)
    ```python
    @dsl.component(base_image='python:3.7',
                target_image='gcr.io/my-project/my-component:v1')
    def add(a: int, b: int) -> int:
        return add_numbers(a, b)
    ```

    - Container Components, unlike Python Components, enable component authors to set the image, command, and args directly. This makes it possible to author components that execute shell scripts, use other languages and binaries, etc., all from within the KFP Python SDK.

- Docker
    - ENTRYPOINT vs. COMMAND
        - https://www.bmc.com/blogs/docker-cmd-vs-entrypoint/
        - CMD is a shell command type
        - With ENTRYPOINT, instructions written in executable form directly runs the executable binaries, without going through shell validation and processing
    - 
