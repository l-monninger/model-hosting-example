export type SidecarLine = [number, string];

export interface ModelConfig {
    width ? : string;
    depth ? : string;
    latency ? : string;
    prompt ? : string
}

export interface StartModelConfig {
    id ? : string;
    prompt ? : string;
}