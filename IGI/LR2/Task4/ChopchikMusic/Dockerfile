FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /back
EXPOSE 5285
EXPOSE 7113

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY [".", "./"]
RUN dotnet restore "/src/prototype/prototype.csproj"
COPY . .
RUN dotnet publish "/src/prototype/prototype.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS="http://+:5285;https://+:7113"
ENTRYPOINT ["dotnet", "prototype.dll"]
