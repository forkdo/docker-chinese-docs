# Docker Build

Docker Build is one of Docker Engine's most used features. Whenever you are
creating an image you are using Docker Build. Build is a key part of your
software development life cycle allowing you to package and bundle your code and
ship it anywhere.

Docker Build is more than a command for building images, and it's not only about
packaging your code. It's a whole ecosystem of tools and features that support
not only common workflow tasks but also provides support for more complex and
advanced scenarios.


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/build/concepts/overview/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-80q-24.75 0-42.37-17.63Q120-115.25 120-140v-483q-17-6-28.5-21.39T80-680v-140q0-24.75 17.63-42.38Q115.25-880 140-880h680q24.75 0 42.38 17.62Q880-844.75 880-820v140q0 20.22-11.5 35.61T840-623v483q0 24.75-17.62 42.37Q804.75-80 780-80H180Zm-40-600h680v-140H140v140Zm250 260h180q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H390q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Packaging your software</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Build and package your application to run it anywhere: locally or in the cloud.</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/build/building/multi-stage/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M407-383h73q12.75 0 21.38-8.63Q510-400.25 510-413v-103h73q12.75 0 21.38-8.63Q613-533.25 613-546v-104h67q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5h-97q-12.75 0-21.37 8.62Q553-692.75 553-680v103h-73q-12.75 0-21.37 8.62Q450-559.75 450-547v103h-73q-12.75 0-21.37 8.62Q347-426.75 347-414v104h-67q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5h97q12.75 0 21.38-8.63Q407-267.25 407-280v-103ZM180-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h600q24 0 42 18t18 42v600q0 24-18 42t-42 18H180Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Multi-stage builds</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Keep your images small and secure with minimal dependencies.</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/build/building/multi-platform/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Multi-platform images</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Build, push, pull, and run images seamlessly on different computer architectures.</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/build/buildkit/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M740-149 517-371l57-57 223 223q12 12 12 28t-12 28q-12 12-28.5 12T740-149Zm-581 0q-12-12-12-28.5t12-28.5l261-261-107-107-2 2q-9 9-21 9t-21-9l-23-23v97q0 10-9.5 13.5T220-488L102-606q-7-7-3.5-16.5T112-632h98l-27-27q-9-9-9-21t9-21l110-110q17-17 37-23t44-6q21 0 36 5.5t32 18.5q5 5 5.5 11t-4.5 11l-95 95 27 27q9 9 9 21t-9 21l-3 3 104 104 122-122q-8-13-12.5-30t-4.5-36q0-53 38.5-91.5T711-841q8 0 14.5.5T737-838q6 3 7.5 9.5T741-817l-61 61q-5 5-5 11t5 11l53 53q5 5 11 5t11-5l59-59q5-5 13-4t11 8q2 6 2.5 12.5t.5 14.5q0 53-38.5 91.5T711-579q-18 0-31-2.5t-24-7.5L215-148q-12 12-28 11.5T159-149Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">BuildKit</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Explore BuildKit, the open source build engine.</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/build/builders/drivers/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M42-150v-62q0-34 16-56.5t45-36.5q54-26 115.5-43T358-365q78 0 139.5 17T613-305q29 14 45 36.5t16 56.5v62q0 13-8.5 21.5T644-120H72q-13 0-21.5-8.5T42-150Zm316-275q-66 0-108-43t-42-107h-10q-8 0-14-6t-6-14q0-8 6-14t14-6h10q0-40 20-72t52-52v39q0 6 4.5 10.5T295-685q7 0 11-4.5t4-10.5v-52q8-2 22-3.5t27-1.5q13 0 27 1.5t22 3.5v52q0 6 4 10.5t11 4.5q6 0 10.5-4.5T438-700v-39q32 20 51 52t19 72h10q8 0 14 6t6 14q0 8-6 14t-14 6h-10q0 64-42 107t-108 43Zm0-60q42 0 66-25t24-65H268q0 40 24 65t66 25Zm301 105-1-10q-7-4-14.5-9T630-409l-11 6q-7 4-13.5 2t-11.5-8l-1-2q-5-7-3.5-14.5T597-438l11-8q-2-4-2-7.5v-15q0-3.5 2-7.5l-11-8q-6-5-7.5-12t3.5-14l1-3q5-6 11.5-8t13.5 2l11 6 14-10q7-5 14-9l1-11q1-8 6.5-13t13.5-5h2q8 0 13.5 5.5T701-542l1 10q7 4 14 9l14 10 11-6q7-4 13.5-2t11.5 8l1 2q5 7 3.5 14.5T763-484l-11 8q2 4 2 7.5v15q0 3.5-2 7.5l11 8q6 5 7.5 12t-3.5 14l-1 3q-5 6-11.5 8t-13.5-2l-11-6q-6 5-13.5 10t-14.5 9l-1 11q-1 8-6.5 13t-13.5 5h-2q-8 0-13.5-5.5T659-380Zm21-43q16 0 27-11t11-27q0-16-11-27t-27-11q-16 0-27 11t-11 27q0 16 11 27t27 11Zm84-169-5-21q-10-4-20.5-11T721-639l-28 10q-7 2-13.5 0t-10.5-8l-4-6q-4-7-2.5-14t7.5-12l22-17q-2-5-3.5-11t-1.5-12q0-6 1.5-12t3.5-11l-22-17q-6-5-7.5-12.5T665-775l4-5q4-6 10.5-8.5t13.5-.5l28 10q7-8 17.5-15.5T759-805l5-21q2-6 7-10t11-4h10q6 0 11 4t7 10l5 21q10 3 20.5 10.5T853-779l28-10q7-2 13.5 0t10.5 8l4 6q4 7 2.5 14t-7.5 12l-22 17q2 5 3.5 11t1.5 12q0 6-1.5 12t-3.5 11l22 17q6 5 7.5 12.5T909-643l-4 5q-4 6-10.5 8.5t-13.5.5l-28-10q-7 8-17.5 15T815-613l-5 21q-2 6-7 10t-11 4h-10q-6 0-11-4t-7-10Zm23-59q25 0 41.5-16.5T845-709q0-25-16.5-41.5T787-767q-25 0-41.5 16.5T729-709q0 25 16.5 41.5T787-651Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Build drivers</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Configure where and how you run your builds.</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/build/exporters/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h600q24 0 42 18t18 42v60q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-60H180v600h600v-60q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v60q0 24-18 42t-42 18H180Zm585-330H390q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h375l-92-93q-8-9-8.5-21.1-.5-12.1 8.5-20.9 9-9 21-9t21 9l144 144q5 5 7 10.13 2 5.14 2 11 0 5.87-2 10.87-2 5-7 10L715-315q-9 9-21 9t-21-9q-9-9-9-21t9-21l92-93Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Exporters</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Export any artifact you like, not just Docker images.</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/build/cache/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-480q0 105 57 190t153 125q12 5 17.5 16.5T367-126q-8 12-21 15.5t-27-2.5q-110-48-174.5-147.5T80-480q0-32 5-64.5t16-63.5l-40 23q-11 6-22.5 3.5T21-595q-6-11-3-23t14-18l121-70q11-6 23-3t18 14l70 120q6 11 3 23t-14 18q-11 6-23 3t-18-14l-43-73q-14 33-21.5 67.5T140-480Zm340-340q-57 0-109.5 18T273-749q-11 8-23.5 7.5T231-753q-7-12-4-26t14-22q52-38 113-58.5T480-880q87 0 165 35.5T780-744v-46q0-13 8.5-21.5T810-820q13 0 21.5 8.5T840-790v140q0 13-8.5 21.5T810-620H670q-13 0-21.5-8.5T640-650q0-13 8.5-21.5T670-680h85q-48-66-120.5-103T480-820Zm252 569q51-57 73-129t11-147q-2-13 5.5-23t19.5-10q14 0 24 10.5t12 25.5q8 81-14 157.5T790-227q-44 54-102 89.5T562-88l38 22q11 6 13.5 18T610-25q-6 11-17.5 13.5T570-15L448-85q-11-6-14-18t3-23l70-120q6-11 18-14t23 3q11 6 13.5 17.5T558-217l-43 76q63-6 119-34.5t98-75.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Build caching</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Avoid unnecessary repetitions of costly operations, such as package installs.</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/build/bake/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M160-80q-17 0-28.5-11.5T120-120v-219q0-24.75 17.63-42.38Q155.25-399 180-399h600q24.75 0 42.38 17.62Q840-363.75 840-339v219q0 17-11.5 28.5T800-80H160Zm47-379v-122q0-24.75 17.63-42.38Q242.25-641 267-641h183v-64q-20-14-30.5-30.53-10.5-16.54-10.5-39.88 0-14.59 5.5-28.09T430-827l39-41q1-1 11.29-5 1.71 0 10.71 5l39 41q10 10 16 23.5t6 28.09q0 23.34-11 39.88Q530-719 510-705v64h183q24.75 0 42.38 17.62Q753-605.75 753-581v122H207Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Bake</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Orchestrate your builds with Bake.</p>
    </div>
  
    </a>
  
</div>

  
</div>



- [Checking your build configuration](https://docs.docker.com/build/checks/)

- [Builders](https://docs.docker.com/build/builders/)

- [Bake](https://docs.docker.com/build/bake/)

- [Docker build cache](https://docs.docker.com/build/cache/)

- [Continuous integration with Docker](https://docs.docker.com/build/ci/)

- [Exporters overview](https://docs.docker.com/build/exporters/)

- [BuildKit](https://docs.docker.com/build/buildkit/)

- [Build release notes](https://docs.docker.com/build/release-notes/)

