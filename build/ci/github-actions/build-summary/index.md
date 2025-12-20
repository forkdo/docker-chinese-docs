# GitHub Actions build summary

Docker's GitHub Actions for building and pushing images generate a job summary
for your build that outlines the execution and materials used:

- A summary showing the Dockerfile used, the build duration, and cache utilization
- Inputs for the build, such as build arguments, tags, labels, and build contexts
- For builds with [Bake](../../bake/_index.md), the full bake definition for the build

![A GitHub Actions build summary](../images/gha_build_summary.png)

Job summaries for Docker builds appear automatically if you use the following
versions of the [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images)
or [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake)
GitHub Actions:

- `docker/build-push-action@v6`
- `docker/bake-action@v6`

To view the job summary, open the details page for the job in GitHub after the
job has finished. The summary is available for both failed and successful
builds. In the case of a failed build, the summary also displays the error
message that caused the build to fail:

![Builds summary error message](../images/build_summary_error.png)

## Import build records to Docker Desktop





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Beta
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M360-360H217q-18 0-26.5-16t2.5-31l338-488q8-11 20-15t24 1q12 5 19 16t5 24l-39 309h176q19 0 27 17t-4 32L388-66q-8 10-20.5 13T344-55q-11-5-17.5-16T322-95l38-265Z"/></svg></span>
            
          
            
          
            
          
            
          
            
          
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="/desktop/release-notes/#4310">4.31</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



The job summary includes a link for downloading a build record archive for the
run. The build record archive is a ZIP file containing the details about a build
(or builds, if you use `docker/bake-action` to build multiple targets). You can
import this build record archive into Docker Desktop, which gives you a
powerful, graphical interface for further analyzing the build's performance via
the [Docker Desktop **Builds** view](/manuals/desktop/use-desktop/builds.md).

To import the build record archive into Docker Desktop:

1. Download and install [Docker Desktop](/get-started/get-docker.md).

2. Download the build record archive from the job summary in GitHub Actions.

3. Open the **Builds** view in Docker Desktop.

4. Select the **Import build** button, and then browse for the `.zip` archive
   job summary that you downloaded. Alternatively, you can drag-and-drop the
   build record archive ZIP file onto the Docker Desktop window after opening
   the import build dialog.

5. Select **Import** to add the build records.

After a few seconds, the builds from the GitHub Actions run appear under the
**Completed builds** tab in the Builds view. To inspect a build and see a
detailed view of all the inputs, results, build steps, and cache utilization,
select the item in the list.

## Disable job summary

To disable job summaries, set the `DOCKER_BUILD_SUMMARY` environment variable
in the YAML configuration for your build step:

```yaml {hl_lines=4}
      - name: Build
        uses: docker/build-push-action@v6
        env:
          DOCKER_BUILD_SUMMARY: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

## Disable build record upload

To disable the upload of the build record archive to GitHub, set the
`DOCKER_BUILD_RECORD_UPLOAD` environment variable in the YAML configuration for
your build step:

```yaml {hl_lines=4}
      - name: Build
        uses: docker/build-push-action@v6
        env:
          DOCKER_BUILD_RECORD_UPLOAD: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

With this configuration, the build summary is still generated, but does not
contain a link to download the build record archive.

## Limitations

Build summaries are currently not supported for:

- Repositories hosted on GitHub Enterprise Servers. Summaries can only be
  viewed for repositories hosted on GitHub.com.

